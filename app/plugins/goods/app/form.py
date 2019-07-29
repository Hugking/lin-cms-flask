from lin import manager
from wtforms import DateTimeField, PasswordField, FieldList, IntegerField, StringField, FloatField, DecimalField, TextField
from wtforms.validators import DataRequired, Regexp, EqualTo, length, Optional, NumberRange
import time

from lin.forms import Form


class CreateCategoryForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])
    keywords = StringField(validators=[DataRequired(message='关键字不能为空')])
    front_name = StringField(validators=[Optional()])
    front_desc = StringField(validators=[Optional()])
    parent_id = StringField(validators=[Optional()])
    sort_order = StringField(validators=[Optional()])
    show_index = StringField(validators=[Optional()])
    banner_url = StringField(validators=[Optional()])
    icon_url = StringField(validators=[Optional()])
    img_url = StringField(validators=[Optional()])
    wap_banner_url = StringField(validators=[Optional()])
    level = StringField(validators=[Optional()])
    type = StringField(validators=[Optional()])


class CreateAttributeCategoryForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])


class SearchAllForm(Form):
    page = StringField(validators=[DataRequired(message='页码不能为空')])
    size = StringField(validators=[DataRequired(message='页数据不能为空')])


class CreateAttrForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])
    attribute_category_id = StringField(validators=[DataRequired(message='属性类不能为空')])
    input_type = StringField(validators=[Optional()])
    values = StringField(validators=[Optional()])
    sort_order = StringField(validators=[Optional()])


class SearchNameForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])


class CreateKeywordsForm(Form):
    is_hot = StringField(validators=[Optional()])
    is_default = StringField(validators=[Optional()])
    is_show = StringField(validators=[Optional()])
    sort_order = StringField(validators=[Optional()])
    scheme_url = StringField(validators=[Optional()])
    type = StringField(validators=[Optional()])


class CreateBrandForm(Form):
    name = StringField(validators=[DataRequired(message='名称不能为空')])
    list_pic_url = StringField(validators=[Optional()])
    simple_desc = StringField(validators=[Optional()])
    pic_url = StringField(validators=[Optional()])
    sort_order = StringField(validators=[Optional()])
    is_show = StringField(validators=[Optional()])
    floor_price = StringField(validators=[Optional()])
    app_list_pic_url = StringField(validators=[Optional()])
    is_new = StringField(validators=[Optional()])
    new_pic_url = StringField(validators=[Optional()])
    new_sort_order = StringField(validators=[Optional()])


class CreateGoodsForm(Form):
    category_id = StringField(validators=[DataRequired(message='分类不能为空')])
    goods_sn = StringField(validators=[Optional()])
    name = StringField(validators=[DataRequired(message='名称不能为空')])
    brand_id = StringField(validators=[DataRequired(message='品牌不能为空')])
    goods_num = StringField(validators=[DataRequired(message='商品数量不能为空')])
    keywords = StringField(validators=[Optional()])
    goods_brief = StringField(validators=[Optional()])
    goods_desc = StringField(validators=[DataRequired(message='商品描述不能为空')])
    is_on_sale = StringField(validators=[Optional()])
    sort_order = StringField(validators=[Optional()])
    is_delete = StringField(validators=[Optional()])
    attribute_category = StringField(validators=[Optional()])
    counter_price = StringField(validators=[Optional()])
    extra_price = StringField(validators=[Optional()])
    is_new = StringField(validators=[Optional()])
    goods_unit = StringField(validators=[DataRequired(message='单位不能为空')])
    primary_pic_url = StringField(validators=[DataRequired(message='主图不能为空')])
    list_pic_url = StringField(validators=[Optional()])
    retail_price = StringField(validators=[Optional()])
    sell_volume = StringField(validators=[Optional()])
    primary_product_id = StringField(validators=[Optional()])
    unit_price = StringField(validators=[DataRequired(message='单价不能为空')])
    promotion_desc = StringField(validators=[Optional()])
    promotion_tag = StringField(validators=[Optional()])
    app_exclusive_price = StringField(validators=[Optional()])
    is_limited = StringField(validators=[Optional()])
    is_hot = StringField(validators=[Optional()])


class CreateGoodsAttrForm(Form):
    goods_id = StringField(validators=[DataRequired(message='商品id不能为空')])
    attribute_id = StringField(validators=[DataRequired(message='属性id不能为空')])
    values = StringField(validators=[Optional()])
