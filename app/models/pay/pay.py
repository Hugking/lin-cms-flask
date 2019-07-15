from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, DateTime, Index, Integer, Numeric, String, Text
from lin.db import db

import hashlib, time, random, decimal, json, requests
from flask import app,request
from app.config.setting import PAY_STATUS_DISPLAY_MAPPING
from app.models.pay.pay_callback import PayCallbackData
from app.models.pay.pay_refund import PayRefund
from app.models.third_client.third_bind import ThirdBind
from app.models.queue.queue_list import QueueList
from app.config.secure import WX_APP,APP
from app.libs.wx_pay import WxPay

from flask import current_app as app

class Pay(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_sn = Column(String(40), nullable=False, unique=True, default=' ')
    member_id = Column(Integer, nullable=False, default='0')
    pay_price = Column(Numeric(10, 2), nullable=False, default='0.00')
    pay_sn = Column(String(128), nullable=False, default=' ')
    prepay_id = Column(String(128), nullable=False, default=' ')
    note = Column(Text, nullable=False, default=' ')
    status = Column(Integer, nullable=False, default='0')
    pay_time = Column(DateTime)

    @property
    def status_desc(self):
        return PAY_STATUS_DISPLAY_MAPPING[str(self.status)]

    @classmethod
    def generate_order_sn(self):
        m = hashlib.md5()
        sn = None
        while True:
            str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
            m.update(str.encode("utf-8"))
            sn = m.hexdigest()
            if not self.query.filter_by(order_sn=sn).first():
                break
        return sn

    @classmethod
    def create_order(self, form):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        pay_price = decimal.Decimal(0.00)
        pay_price = pay_price + decimal.Decimal(form.price.data)
        model_pay = self.create(
            order_sn = self.generate_order_sn(),
            member_id = form.member_id.data,
            pay_price = pay_price,
            note = form.note.data,
            status = 0,
            commit=True
        )
        resp['data'] = {
            'id': model_pay.id,
            'order_sn': model_pay.order_sn,
            'pay_price': str(pay_price)
        }
        return resp
    
    @classmethod
    def close_order(self, pay_id=0):
        if pay_id < 1:
            return False
        pay_order_info = self.query.filter_by(id=pay_id, status=0).first()
        if not pay_order_info:
            return False
            
        pay_order_info.status = -2
        db.session.add(pay_order_info)
        db.session.commit()
        return True

    @classmethod
    def order_pay(cls, form):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        pay_order_info = cls.query.filter_by( order_sn = form.order_sn.data,member_id = form.member_id.data, delete_time=None).first()
        bind_info = ThirdBind.query.filter_by( member_id = form.member_id.data, delete_time=None).first()
        if pay_order_info is not None and bind_info is not None:
            config_mina = WX_APP
            notify_url = APP['domain'] + config_mina['callback_url']
            target_wechat = WxPay( merchant_key=config_mina['paykey'] )
            data = {
                'appid': config_mina['appid'],
                'mch_id': config_mina['mch_id'],
                'nonce_str': target_wechat.get_nonce_str(),
                'body': '测试支付'+pay_order_info.note,  # 商品描述
                'out_trade_no': pay_order_info.order_sn,  # 商户订单号
                'total_fee': int( pay_order_info.pay_price * 100 ),# 以分为单位（int）
                'notify_url': notify_url,# 通知地址
                'trade_type': "JSAPI",
                'openid': bind_info.openid
            }
            pay_info = target_wechat.get_pay_info( pay_data=data)
            #保存prepay_id为了后面发模板消息
            pay_order_info.prepay_id = pay_info['prepay_id']
            db.session.add( pay_order_info )
            db.session.commit()
            resp['data']['pay_info'] = pay_info
            return resp
            
        resp['code'] = -1
        resp['msg'] = "未查询到用户订单，请稍后重试"
        return resp
    
    @classmethod
    def order_pay_refund(cls, form):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        pay_order_info = cls.query.filter_by( order_sn = form.order_sn.data,member_id = form.member_id.data, delete_time=None).first()
        if pay_order_info is not None:
            model_pay_refund = PayRefund.create(
                pay_id = pay_order_info.id,
                refund_sn = form.refund_sn.data if form.refund_sn.data else cls.generate_order_sn(),
                refund_fee = form.refund_fee.data,
                refund_desc = form.refund_desc.data,
                status = 0,
                commit=True
            )
            config_mina = WX_APP
            notify_url = APP['domain'] + config_mina['refund_url']
            target_wechat = WxPay( merchant_key=config_mina['paykey'] )
            data = {
                'appid': config_mina['appid'],
                'mch_id': config_mina['mch_id'],
                'nonce_str': target_wechat.get_nonce_str(),
                'refund_desc': '测试退款' + form.refund_desc.data,  # 退款原因
                'out_trade_no': pay_order_info.order_sn,  # 商户订单号
                'out_refund_no':model_pay_refund.refund_sn,# 商户退款单号
                'total_fee': int( pay_order_info.pay_price * 100 ),# 订单金额以分为单位（int）
                'refund_fee':int(model_pay_refund.refund_fee * 100),# 退款金额以分为单位int
                'notify_url': notify_url# 通知地址
            }
            pay_info = target_wechat.get_pay_reund_info(pay_data = data)
            resp['data']['pay_info'] = pay_info
            return resp

        resp['code'] = -1
        resp['msg'] = "未查询到用户订单，请稍后重试"
        return resp
    
    @classmethod
    def order_success(self, pay_id=0, params=None):
        try:
            pay_order_info = self.query.filter_by(id=pay_id).first()
            if not pay_order_info or pay_order_info.status is not 0:
                return True

            pay_order_info.pay_sn = params['pay_sn'] if params and 'pay_sn' in params else ''
            pay_order_info.status = 1
            db.session.add(pay_order_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            return False

        # 加入通知队列，做消息提醒和
        QueueList.add_queue("pay", {
            "member_id": pay_order_info.member_id,
            "pay_id": pay_order_info.id
        })
        return True

    @classmethod
    def refund_success(self, pay_id=0,refund_sn=None):
        try:
            pay_refund_info = PayRefund.query.filter_by(id=pay_id,refund_sn=refund_sn).first()
            if not pay_refund_info or pay_refund_info.status is not 0:
                return True

            pay_order_info = self.query.filter_by(id=pay_id).first()
            if not pay_order_info or pay_order_info.status is not 2:
                return True

            pay_order_info.status = 2
            pay_refund_info.status = 1
            db.session.add(pay_order_info)
            db.session.add(pay_refund_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            return False

        # 加入通知队列，做消息提醒和
        QueueList.add_queue("refund", {
        "member_id": pay_order_info.member_id,
        "pay_id": pay_order_info.id,
        'refund_id':pay_refund_info.id
        })
        return True


    @classmethod
    def add_callback(self, pay_id=0, type='pay', data=''):
        model_callback = PayCallbackData()
        model_callback.pay_id = pay_id
        if type == "pay":
            model_callback.pay_data = data
            model_callback.refund_data = ''
        else:
            model_callback.refund_data = data
            model_callback.pay_data = ''
            
        db.session.add(model_callback)
        db.session.commit()
        return True
    
    @classmethod
    def send_message(cls):
        list = QueueList.query.filter_by(status = -1 )\
            .order_by( QueueList.id.asc() ).limit(1).all()
        for item in list:
            if item.queue_name == "pay":
                item.status = 1
                db.session.add( item )
                db.session.commit()
                return cls.handlePay( item )
    
    @classmethod
    def handlePay(cls, item):
        data = json.loads( item.data )
        if 'member_id' not in data or 'pay_id' not in data:
            return False

        bind_info = ThirdBind.query.filter_by(member_id=data['member_id']).first()
        if not bind_info:
            return False
            
        pay_order_info = cls.query.filter_by( id = data['pay_id']).first()
        if not pay_order_info:
            return False
        
        keyword1_val = pay_order_info.note if pay_order_info.note else '无'
        keyword2_val = pay_order_info.order_sn
        keyword3_val = str( pay_order_info.pay_price )
        target_wechat = WxPay( )
        access_token = target_wechat.get_access_token()
        headers = {'Content-Type': 'application/json'}
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s"%access_token
        params = {
            "touser": bind_info.openid,
            "template_id":"qT2ghb8Mlvd9BSk-BpDeiElZM0CcCgzXQOffiWSY-DU",
            "page": "pages/my/order_list",
            "form_id": pay_order_info.prepay_id,
            "data": {
                "keyword1": {
                    "value": keyword1_val
                },
                "keyword2": {
                    "value": keyword2_val
                },
                "keyword3": {
                    "value": keyword3_val
                }
            }
        }

        r = requests.post(url=url, data= json.dumps( params ).encode('utf-8'), headers=headers)
        r.encoding = "utf-8"
        return True
    
    @classmethod
    def handlePayRefund(cls, item):
        data = json.loads( item.data )
        if 'member_id' not in data or 'pay_id' not in data:
            return False

        bind_info = ThirdBind.query.filter_by(member_id=data['member_id']).first()
        if not bind_info:
            return False
            
        pay_order_info = cls.query.filter_by( id = data['pay_id']).first()
        if not pay_order_info:
            return False
        
        pay_refund_info = PayRefund.query.filter_by( id = data['refund_id']).first()
        if not pay_refund_info:
            return False
        
        keyword1_val = pay_refund_info.refund_desc if pay_refund_info.refund_desc else '无'
        keyword2_val = pay_refund_info.refund_sn
        keyword3_val = str( pay_refund_info.refund_fee )
        target_wechat = WxPay( )
        access_token = target_wechat.get_access_token()
        headers = {'Content-Type': 'application/json'}
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s"%access_token
        params = {
            "touser": bind_info.openid,
            "template_id":"qT2ghb8Mlvd9BSk-BpDeiElZM0CcCgzXQOffiWSY-DU",
            "page": "pages/my/order_list",
            "form_id": pay_order_info.prepay_id,
            "data": {
                "keyword1": {
                    "value": keyword1_val
                },
                "keyword2": {
                    "value": keyword2_val
                },
                "keyword3": {
                    "value": keyword3_val
                }
            }
        }

        r = requests.post(url=url, data= json.dumps( params ).encode('utf-8'), headers=headers)
        r.encoding = "utf-8"
        return True