
"""
    :copyright: © 2019 by the wkaanig.
    :license: MIT, see LICENSE for more details.
"""
import hashlib, time, random, decimal, json, requests, string
from ..model import *
from .wx_pay import WxPay
from lin.core import lin_config
wx_app = lin_config.get_config('wx.wx_app')
pay_status_display_mapping = lin_config.get_config('wx.pay_status_display_mapping')
pay_refund_status_display_mapping = lin_config.get_config('wx.pay_refund_status_display_mapping')
from flask import current_app as app

class ThirdBind(ThirdBind): 
    @classmethod
    def get_wechat_openid(cls,form):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(wx_app['appid'], wx_app['app_secret'], form.code.data)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        else:
            return -1
        return openid

    @classmethod
    def wx_check_openid(cls, form):
        resp = {'code': 200, 'msg': '????~', 'data': {}}
        openid = cls.get_wechat_openid(form)
        if openid is None:
            resp['code'] = -1
            resp['msg'] = "??????"
            return resp
        if openid is -1:
            resp['code'] = -2
            resp['msg'] = "code???"
            return resp
        return openid

    @classmethod
    def wx_check_reg(cls, form):
        resp = {'code': 200, 'msg': '????~', 'data': {}}
        openid = cls.wx_check_openid(form)
        bind_info = cls.query.filter_by(openid=openid, delete_time=None).first()
        if bind_info is None:
            resp['code'] = -1
            resp['msg'] = "???"
            return resp
        member_info = Member.query.filter_by(id=bind_info.member_id, delete_time=None).first()
        if member_info is None:
            resp['code'] = -1
            resp['msg'] = "????????"
            return resp
        token = "%s#%s" % (cls.generate_auth_code(member_info), member_info.id)
        resp['data'] = {'token': token}
        resp['data']['info'] = {
        "member_id":member_info.id,
        "nickname": member_info.nickname,
        "avatar_url": member_info.avatar
        }
        return resp
    
    @classmethod
    def wx_register(cls, form):
        resp = {'code': 200, 'msg': '????~', 'data': {}}
        openid = cls.wx_check_openid(form)
        bind_info = cls.query.filter_by(openid=openid, delete_time=None).first()
        if bind_info is not None:
            member_info = Member.query.filter_by(id=bind_info.member_id, delete_time=None).first()
            if member_info is None:
                resp['code'] = -1
                resp['msg'] = "????????"
                return resp
        member_info = Member.create(
            nickname = form.userInfo.data['nickName'],
            sex=form.userInfo.data['gender'],
            avatar = form.userInfo.data['avatarUrl'],
            salt = cls.generate_salt(),
            commit=True
        )
        cls.create(
            member_id = member_info.id,
            client_type = 'wx',
            openid = openid,
            commit=True
        )
        token = "%s#%s" % (cls.generate_auth_code(member_info), member_info.id)
        resp['data'] = {'token': token}
        resp['data']['info'] = {
        "member_id":member_info.id,
        "nickname": member_info.nickname,
        "avatar_url": member_info.avatar
        }
        return resp

    @staticmethod
    def generate_auth_code(member_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def generate_salt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(keylist)

class Pay(Pay):
    @property
    def status_desc(self):
        return pay_status_display_mapping[str(self.status)]

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
        resp = {'code': 200, 'msg': '????~', 'data': {}}
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
        resp = {'code': 200, 'msg': '????~', 'data': {}}
        pay_order_info = cls.query.filter_by( order_sn = form.order_sn.data,member_id = form.member_id.data, delete_time=None).first()
        bind_info = ThirdBind.query.filter_by( member_id = form.member_id.data, delete_time=None).first()
        if pay_order_info is not None and bind_info is not None:
            config_mina = wx_app
            notify_url = config_mina['callback_url']
            target_wechat = WxPay( merchant_key=config_mina['paykey'] )
            data = {
                'appid': config_mina['appid'],
                'mch_id': config_mina['mch_id'],
                'nonce_str': target_wechat.get_nonce_str(),
                'body': '????'+pay_order_info.note,  # ????
                'out_trade_no': pay_order_info.order_sn,  # ?????
                'total_fee': int( pay_order_info.pay_price * 100 ),# ??????int?
                'notify_url': notify_url,# ????
                'trade_type': "JSAPI",
                'openid': bind_info.openid
            }
            pay_info = target_wechat.get_pay_info( pay_data=data)
            #??prepay_id?????????
            pay_order_info.prepay_id = pay_info['prepay_id']
            db.session.add( pay_order_info )
            db.session.commit()
            resp['data']['pay_info'] = pay_info
            return resp
            
        resp['code'] = -1
        resp['msg'] = "??????????????"
        return resp
    
    @classmethod
    def order_pay_refund(cls, form):
        resp = {'code': 200, 'msg': '????~', 'data': {}}
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
            config_mina = wx_app
            notify_url = config_mina['refund_url']
            target_wechat = WxPay( merchant_key=config_mina['paykey'] )
            data = {
                'appid': config_mina['appid'],
                'mch_id': config_mina['mch_id'],
                'nonce_str': target_wechat.get_nonce_str(),
                'refund_desc': '????' + form.refund_desc.data,  # ????
                'out_trade_no': pay_order_info.order_sn,  # ?????
                'out_refund_no':model_pay_refund.refund_sn,# ??????
                'total_fee': int( pay_order_info.pay_price * 100 ),# ??????????int?
                'refund_fee':int(model_pay_refund.refund_fee * 100),# ?????????int
                'notify_url': notify_url# ????
            }
            pay_info = target_wechat.get_pay_reund_info(pay_data = data)
            resp['data']['pay_info'] = pay_info
            return resp

        resp['code'] = -1
        resp['msg'] = "??????????????"
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

        # ?????????????
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

        # ?????????????
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
        
        keyword1_val = pay_order_info.note if pay_order_info.note else '?'
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
        
        keyword1_val = pay_refund_info.refund_desc if pay_refund_info.refund_desc else '?'
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

class PayRefund(PayRefund):
    @property
    def status_desc(self):
        return pay_refund_status_display_mapping[str(self.status)]

class QueueList(QueueList):
    @classmethod
    def add_queue(cls, queue_name, data=None):
        model_queue = QueueList()
        model_queue.queue_name = queue_name
        if data:
            model_queue.data = json.dumps(data)
        db.session.add(model_queue)
        db.session.commit()
        return True
    
