
"""
    :copyright: © 2019 by the wkaanig.
    :license: MIT, see LICENSE for more details.
"""

from .form import *
from lin.redprint import Redprint
from flask import jsonify, request
from ..app.interface.wx import *
from lin.core import lin_config
wx_app = lin_config.get_config('wx.wx_app')
wx_api = Redprint("wx")


@wx_api.route("/", methods=["GET"])
def test():
    return "hi, guy!"


@wx_api.route('/check-reg', methods=['POST'])
def checkReg():
    form = ThirdClientForm().validate_for_api()
    resp = ThirdBind.wx_check_reg(form)
    return jsonify(resp)


@wx_api.route('/login', methods=['POST'])
def login():
    form = WxClientForm().validate_for_api()
    resp = ThirdBind.wx_register(form)
    return jsonify(resp)


@wx_api.route('/create', methods=["POST"])
def pay_create():
    """
        ??????
        input 'member_id' 'price' 'note'
        output 'id''order_sn''pay_price'
    """
    form = PayCreateForm().validate_for_api()
    resp = Pay.create_order(form)
    return jsonify(resp)


@wx_api.route('/pay', methods=["POST"])
def orderPay():
    """
        ??
        input 'order_sn' 'member_id' 
        output '????'
    """
    form = PayForm().validate_for_api()
    resp = Pay.order_pay(form)
    return jsonify(resp)


@wx_api.route('/callback', methods=["POST", "GET"])
def orderCallback():
    result_data = {'return_code': 'SUCCESS', 'return_msg': 'OK'}
    header = {'Content-Type': 'application/xml'}
    config_mina = wx_app
    target_wechat = WxPay(merchant_key=config_mina['paykey'])
    callback_data = target_wechat.xml_to_dict(request.data)
    app.logger.info(callback_data)
    sign = callback_data['sign']
    callback_data.pop('sign')
    gene_sign = target_wechat.create_sign(callback_data)
    app.logger.info(gene_sign)
    if sign != gene_sign:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    if callback_data['result_code'] != 'SUCCESS':
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    order_sn = callback_data['out_trade_no']
    pay_order_info = Pay.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    if int(pay_order_info.pay_price * 100) != int(callback_data['total_fee']):
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    if pay_order_info.status == 1:
        return target_wechat.dict_to_xml(result_data), header

    Pay.order_success(pay_id=pay_order_info.id, params={"pay_sn": callback_data['transaction_id']})
    Pay.add_callback(pay_id=pay_order_info.id, data=request.data)
    return target_wechat.dict_to_xml(result_data), header


@wx_api.route('/rcallback', methods=["POST", "GET"])
def refundCallback():
    result_data = {'return_code': 'SUCCESS', 'return_msg': 'OK'}
    header = {'Content-Type': 'application/xml'}
    config_mina = wx_app
    target_wechat = WxPay(merchant_key=config_mina['paykey'])
    callback_data = target_wechat.xml_to_dict(request.data)
    app.logger.info(callback_data)

    if callback_data['return_code'] != 'SUCCESS':
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    return target_wechat.dict_to_xml(result_data), header


@wx_api.route('/payrefund', methods=['POST'])
def orderRefund():
    """
        ????
        input 'order_sn' 'member_id' 'refund_fee' 'refund_desc'
        output '????'  
    """
    form = PayRefundForm().validate_for_api()
    resp = Pay.order_pay_refund(form)
    return jsonify(resp)


@wx_api.route('/send', methods=["POST", "GET"])
def send_message():
    test = Pay.send_message()
    return jsonify(test)


# @order_api.route('/ops', methods=["POST"])
# def orderOps():
# 	resp = {'code': 200, 'msg': '????~', 'data': {}}
# 	form = OrderPayOpsForm().validate_for_api()
# 	pay_order_info = cls.query.filter_by(order_sn=form.order_sn.data, member_id=form.member_id.data,  delete_time=None).first()
# 	if pay_order_info is None:
# 		resp['code'] = -1
# 		resp['msg'] = "??????????"
# 		return jsonify(resp)
# 	if act == "cancel":
# 		target_pay = PayService( )
# 		ret = target_pay.close_order(pay_id=pay_order_info.id)
# 		if ret is None:
# 			resp['code'] = -1
# 			resp['msg'] = "??????????"
# 			return jsonify(resp)
# 	elif act == "confirm":
# 		pay_order_info.express_status = 1
# 		pay_order_info.updated_time = get_current_date()
# 		db.session.add( pay_order_info )
# 		db.session.commit()
# 	return jsonify(resp)
