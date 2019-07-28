from flask import jsonify,app,json,request
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.pay.pay import Pay
from app.models.pay.pay_refund import PayRefund
from app.validators.forms import PayCreateForm, PayForm, PayRefundForm
from app.config.secure import WX_APP
from app.libs.wx_pay import WxPay
from flask import current_app as app
from app.models.queue.queue_list import QueueList

pay_api = Redprint('pay')

@pay_api.route('/create', methods=["POST"])
def pay_create():
    """
        创建支付订单
        input 'member_id' 'price' 'note'
        output 'id''order_sn''pay_price'
    """
    form = PayCreateForm().validate_for_api()
    resp = Pay.create_order(form)
    return jsonify(resp)
    
@pay_api.route('/pay', methods=["POST"])
def orderPay():
    """
        支付
        input 'order_sn' 'member_id' 
        output '支付详情'
    """
    form = PayForm().validate_for_api()
    resp = Pay.order_pay(form)
    return jsonify(resp)

@pay_api.route('/callback', methods=["POST","GET"])
def orderCallback():
	result_data = {'return_code': 'SUCCESS','return_msg': 'OK'}
	header = {'Content-Type': 'application/xml'}
	config_mina = WX_APP
	target_wechat = WxPay(merchant_key=config_mina['paykey'])
	callback_data = target_wechat.xml_to_dict( request.data )
	app.logger.info( callback_data )
	sign = callback_data['sign']
	callback_data.pop( 'sign' )
	gene_sign = target_wechat.create_sign( callback_data )
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

	if int( pay_order_info.pay_price * 100  ) != int( callback_data['total_fee'] ):
		result_data['return_code'] = result_data['return_msg'] = 'FAIL'
		return target_wechat.dict_to_xml(result_data), header

	if pay_order_info.status == 1:
		return target_wechat.dict_to_xml(result_data), header

	Pay.order_success(pay_id = pay_order_info.id, params = {"pay_sn":callback_data['transaction_id']})
	Pay.add_callback(pay_id = pay_order_info.id, data = request.data)
	return target_wechat.dict_to_xml(result_data), header

@pay_api.route('/rcallback', methods=["POST","GET"])
def refundCallback():
	result_data = {'return_code': 'SUCCESS','return_msg': 'OK'}
	header = {'Content-Type': 'application/xml'}
	config_mina = WX_APP
	target_wechat = WxPay(merchant_key=config_mina['paykey'])
	callback_data = target_wechat.xml_to_dict( request.data )
	app.logger.info( callback_data )

	if callback_data['return_code'] != 'SUCCESS':
		result_data['return_code'] = result_data['return_msg'] = 'FAIL'
		return target_wechat.dict_to_xml(result_data), header

	return target_wechat.dict_to_xml(result_data), header

@pay_api.route('/payrefund',methods=['POST'])
def orderRefund():
    """
        退款接口
        input 'order_sn' 'member_id' 'refund_fee' 'refund_desc'
        output '退款详情'  
    """
    form = PayRefundForm().validate_for_api()
    resp = Pay.order_pay_refund(form)
    return jsonify(resp)

@pay_api.route('/test', methods=["POST","GET"])
def test():
	test = Pay.send_message()
	return jsonify(test)


# @order_api.route('/ops', methods=["POST"])
# def orderOps():
# 	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
# 	form = OrderPayOpsForm().validate_for_api()
# 	pay_order_info = cls.query.filter_by(order_sn=form.order_sn.data, member_id=form.member_id.data,  delete_time=None).first()
# 	if pay_order_info is None:
# 		resp['code'] = -1
# 		resp['msg'] = "系统繁忙。请稍后再试"
# 		return jsonify(resp)
# 	if act == "cancel":
# 		target_pay = PayService( )
# 		ret = target_pay.close_order(pay_id=pay_order_info.id)
# 		if ret is None:
# 			resp['code'] = -1
# 			resp['msg'] = "系统繁忙。请稍后再试"
# 			return jsonify(resp)
# 	elif act == "confirm":
# 		pay_order_info.express_status = 1
# 		pay_order_info.updated_time = get_current_date()
# 		db.session.add( pay_order_info )
# 		db.session.commit()
# 	return jsonify(resp)
	
