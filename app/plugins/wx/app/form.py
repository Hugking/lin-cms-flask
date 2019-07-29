from lin import manager
from wtforms import DateTimeField, PasswordField, FieldList, IntegerField, StringField, FloatField, DecimalField, TextField
from wtforms.validators import DataRequired, Regexp, EqualTo, length, Optional, NumberRange
import time

from lin.forms import Form


class ThirdClientForm(Form):
    code = StringField(validators=[DataRequired(message='必须传入code')])


class WxClientForm(Form):
    code = StringField(validators=[DataRequired(message='必须传入code')])
    userInfo = StringField(validators=[DataRequired(message='用户信息不可为空')])


class PayCreateForm(Form):
    member_id = IntegerField('会员id', validators=[DataRequired(
        message='请传入会员id'), NumberRange(message='会员id必须大于0', min=1)])
    price = StringField('price', validators=[DataRequired(message='价格不能为空')])
    note = StringField(validators=[DataRequired(message='商品描述不可为空')])


class PayForm(Form):
    member_id = IntegerField('会员id', validators=[DataRequired(
        message='请传入会员id'), NumberRange(message='会员id必须大于0', min=1)])
    order_sn = StringField(validators=[DataRequired(message='请传入订单编号')])


class PayRefundForm(Form):
    member_id = IntegerField('会员id', validators=[DataRequired(
        message='请传入会员id'), NumberRange(message='会员id必须大于0', min=1)])
    order_sn = StringField(validators=[DataRequired(message='请传入订单编号')])
    refund_sn = StringField(validators=[Optional()])
    refund_fee = StringField(validators=[DataRequired(message='退款金额不能为空')])
    refund_desc = TextField(validators=[DataRequired(message='退款原因不能为空')])
