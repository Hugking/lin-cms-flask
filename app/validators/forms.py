"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from lin import manager
from wtforms import DateTimeField, PasswordField, FieldList, IntegerField, StringField, FloatField, DecimalField, TextField
from wtforms.validators import DataRequired, Regexp, EqualTo, length, Optional, NumberRange
import time

from lin.forms import Form


# 注册校验
class RegisterForm(Form):
    password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])
    nickname = StringField(validators=[DataRequired(message='昵称不可为空'),
                                       length(min=2, max=10, message='昵称长度必须在2~10之间')])

    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])

    def validate_group_id(self, value):
        exists = manager.group_model.get(id=value.data)
        if not exists:
            raise ValueError('分组不存在')


# 登陆校验
class LoginForm(Form):
    nickname = StringField(validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(message='密码不可为空')])


# 重置密码校验
class ResetPasswordForm(Form):
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')
    ])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])


# 更改密码校验
class ChangePasswordForm(ResetPasswordForm):
    old_password = PasswordField('原密码', validators=[DataRequired(message='不可为空')])


# 管理员创建分组
class NewGroup(Form):
    # 分组name
    name = StringField(validators=[DataRequired(message='请输入分组名称')])
    # 非必须
    info = StringField(validators=[Optional()])
    # 必填，分组的权限
    auths = FieldList(StringField(validators=[DataRequired(message='请输入auths字段')]))


# 管理员更新分组
class UpdateGroup(Form):
    # 分组name
    name = StringField(validators=[DataRequired(message='请输入分组名称')])
    # 非必须
    info = StringField(validators=[Optional()])


class DispatchAuths(Form):
    # 为用户分配的权限
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    auths = FieldList(StringField(validators=[DataRequired(message='请输入auths字段')]))


class DispatchAuth(Form):
    # 为用户分配的权限
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    # 用户查询自己信息
    auth = StringField(validators=[DataRequired(message='请输入auth字段')])


# 批量删除权限
class RemoveAuths(Form):
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    auths = FieldList(StringField(validators=[DataRequired(message='请输入auths字段')]))


# 日志查找范围校验
class LogFindForm(Form):
    # name可选，若无则表示全部
    name = StringField(validators=[Optional()])
    # 2018-11-01 09:39:35
    start = DateTimeField(validators=[])
    end = DateTimeField(validators=[])

    def validate_start(self, value):
        if value.data:
            try:
                _ = time.strptime(value.data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise e

    def validate_end(self, value):
        if value.data:
            try:
                _ = time.strptime(value.data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise e


class EventsForm(Form):
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    events = FieldList(StringField(validators=[DataRequired(message='请输入events字段')]))


# 更新用户邮箱
class UpdateInfoForm(Form):
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])


# 更新用户信息
class UpdateUserInfoForm(Form):
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])


class AvatarUpdateForm(Form):
    avatar = StringField('头像', validators=[
        DataRequired(message='请输入头像url')
    ])


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired(message='必须传入搜索关键字')])  # 前端的请求参数中必须携带`q`


class CreateOrUpdateBookForm(Form):
    title = StringField(validators=[DataRequired(message='必须传入图书名')])
    author = StringField(validators=[DataRequired(message='必须传入图书作者')])
    summary = StringField(validators=[DataRequired(message='必须传入图书综述')])
    image = StringField(validators=[DataRequired(message='必须传入图书插图')])


class ThirdClientForm(Form):
    code = StringField(validators=[DataRequired(message='必须传入code')])

class WxClientForm(Form):
    code = StringField(validators=[DataRequired(message='必须传入code')])
    userInfo = StringField(validators=[DataRequired(message='用户信息不可为空')])

class PayCreateForm(Form):
    member_id = IntegerField('会员id',validators=[DataRequired(message='请传入会员id'), NumberRange(message='会员id必须大于0', min=1)])
    price = StringField('price', validators=[DataRequired(message='价格不能为空')])
    note = StringField(validators=[DataRequired(message='商品描述不可为空')])

class PayForm(Form):
    member_id = IntegerField('会员id',validators=[DataRequired(message='请传入会员id'), NumberRange(message='会员id必须大于0', min=1)])
    order_sn = StringField(validators=[DataRequired(message='请传入订单编号')])

class PayRefundForm(Form):
    member_id = IntegerField('会员id',validators=[DataRequired(message='请传入会员id'), NumberRange(message='会员id必须大于0', min=1)])
    order_sn = StringField(validators=[DataRequired(message='请传入订单编号')])
    refund_sn = StringField()
    refund_fee = StringField(validators=[DataRequired(message='退款金额不能为空')])
    refund_desc = TextField(validators=[DataRequired(message='退款原因不能为空')])

class CreateCategoryForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])
    keywords = StringField(validators=[DataRequired(message='关键字不能为空')])
    front_name = StringField()
    front_desc = StringField()
    parent_id = StringField()
    sort_order = StringField()
    show_index = StringField()
    banner_url = StringField()
    icon_url  = StringField()
    img_url = StringField()
    wap_banner_url = StringField()
    level = StringField()
    type = StringField()

class CreateAttributeCategoryForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])

class SearchAllForm(Form):
    page = StringField(validators=[DataRequired(message='页码不能为空')])
    size = StringField(validators=[DataRequired(message='页数据不能为空')])

class CreateAttrForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])
    attribute_category_id = StringField(validators=[DataRequired(message='属性类不能为空')])
    input_type = StringField()
    values = StringField()
    sort_order = StringField()

class SearchNameForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])

class CreateKeywordsForm(Form):
    is_hot = StringField()
    is_default = StringField()
    is_show = StringField()
    sort_order = StringField()
    scheme_url = StringField()
    type = StringField()

class CreateBrandForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])
    list_pic_url = StringField()
    simple_desc = StringField()
    pic_url = StringField()
    sort_order = StringField()
    is_show = StringField()
    floor_price = StringField()
    app_list_pic_url = StringField()
    is_new = StringField()
    new_pic_url = StringField()
    new_sort_order = StringField()

class CreateGoodsForm(Form):
    category_id = StringField(validators=[DataRequired(message='分类不能为空')])
    goods_sn = StringField()
    name = StringField(validators=[DataRequired(message='名称不能为空')])
    brand_id = StringField(validators=[DataRequired(message='品牌不能为空')])
    goods_num = StringField(validators=[DataRequired(message='商品数量不能为空')])
    keywords = StringField()
    goods_brief = StringField()
    goods_desc = StringField(validators=[DataRequired(message='商品描述不能为空')])
    is_on_sale = StringField()
    sort_order = StringField()
    is_delete = StringField()
    attribute_category = StringField()
    counter_price = StringField()
    extra_price = StringField()
    is_new = StringField()
    goods_unit = StringField(validators=[DataRequired(message='单位不能为空')])
    primary_pic_url = StringField(validators=[DataRequired(message='主图不能为空')])
    list_pic_url = StringField()
    retail_price = StringField()
    sell_volume = StringField()
    primary_product_id = StringField()
    unit_price = StringField(validators=[DataRequired(message='单价不能为空')])
    promotion_desc = StringField()
    promotion_tag = StringField()
    app_exclusive_price = StringField()
    is_limited = StringField()
    is_hot = StringField()