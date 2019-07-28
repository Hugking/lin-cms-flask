from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.validators.forms import ThirdClientForm,WxClientForm
from app.models.third_client.third_bind import ThirdBind

member_api = Redprint('member')

@member_api.route('/check-reg', methods=['POST'])
def checkReg():
    form = ThirdClientForm().validate_for_api()
    resp = ThirdBind.wx_check_reg(form)
    return jsonify(resp)

@member_api.route('/login', methods=['POST'])
def login():
    form = WxClientForm().validate_for_api()
    resp = ThirdBind.wx_register(form)
    return jsonify(resp)
