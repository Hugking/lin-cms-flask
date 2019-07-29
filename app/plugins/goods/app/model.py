from lin import db
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text


class Attribute(Base):
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True)
    attribute_category_id = Column(Integer, nullable=False, index=True)
    name = Column(String(60), nullable=False)
    input_type = Column(Integer, nullable=False)
    values = Column(Text, nullable=False)
    sort_order = Column(Integer, nullable=False)

    @property
    def get_attr_cate(cls):
        attribute_category = AttributeCategory.query.filter_by(id=cls.attribute_category_id, delete_time=None).first()
        if attribute_category is None:
            return '无匹配'
        return attribute_category.name


class AttributeCategory(Base):
    __tablename__ = 'attribute_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    list_pic_url = Column(String(255), nullable=False)
    simple_desc = Column(String(255), nullable=False)
    pic_url = Column(String(255), nullable=False)
    sort_order = Column(Integer, nullable=False)
    is_show = Column(Integer, nullable=False, index=True)
    floor_price = Column(Numeric(10, 2), nullable=False)
    app_list_pic_url = Column(String(255), nullable=False)
    is_new = Column(Integer, nullable=False)
    new_pic_url = Column(String(255), nullable=False)
    new_sort_order = Column(Integer, nullable=False)


class Keywords(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_hot = Column(Integer, index=True, nullable=False, default='0')
    is_default = Column(Integer, index=True, nullable=False, default='0')
    is_show = Column(Integer, index=True, nullable=False, default='1')
    sort_order = Column(Integer, index=True, nullable=False, default='100')
    scheme_url = Column(String(255), index=True, nullable=False, default='')  # è·³è½¬è¿žæŽ¥
    type = Column(Integer, index=True, nullable=False, default='0')


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(90), nullable=False)
    keywords = Column(String(255), nullable=False)
    front_desc = Column(String(255), nullable=False)
    parent_id = Column(Integer, nullable=False, index=True)
    sort_order = Column(Integer, nullable=False)
    show_index = Column(Integer, nullable=False)
    banner_url = Column(String(255), nullable=False)
    icon_url = Column(String(255), nullable=False)
    img_url = Column(String(255), nullable=False)
    wap_banner_url = Column(String(255), nullable=False)
    level = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False)
    front_name = Column(String(255), nullable=False)


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, nullable=False, index=True)
    goods_sn = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    brand_id = Column(Integer, nullable=False, index=True)
    goods_num = Column(Integer, nullable=False, index=True)
    keywords = Column(String(255), nullable=False)
    goods_brief = Column(String(255), nullable=False)
    goods_desc = Column(Text)
    is_on_sale = Column(Integer, nullable=False)
    sort_order = Column(Integer, nullable=False, index=True)
    is_delete = Column(Integer, nullable=False)
    attribute_category = Column(Integer, nullable=False, index=True)
    counter_price = Column(Numeric(10, 2), nullable=False)
    extra_price = Column(Numeric(10, 2), nullable=False)
    is_new = Column(Integer, nullable=False)
    goods_unit = Column(String(255), nullable=False)
    primary_pic_url = Column(String(255), nullable=False)
    list_pic_url = Column(String(255), nullable=False)
    retail_price = Column(Numeric(10, 2), nullable=False)
    sell_volume = Column(Integer, nullable=False)
    primary_product_id = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    promotion_desc = Column(String(255), nullable=False)
    promotion_tag = Column(String(255), nullable=False)
    app_exclusive_price = Column(Numeric(10, 2), nullable=False)
    is_app_exclusive = Column(Integer, nullable=False)
    is_limited = Column(Integer, nullable=False)
    is_hot = Column(Integer, nullable=False)


class GoodsAttribute(Base):
    __tablename__ = 'goods_attribute'

    id = Column(Integer, primary_key=True)
    goods_id = Column(Integer, nullable=False, index=True)
    attribute_id = Column(Integer, nullable=False, index=True)
    values = Column(Text)


class RelatedGoods(Base):
    __tablename__ = 'related_goods'

    id = Column(Integer, primary_key=True)
    goods_id = Column(Integer, nullable=False, index=True)
    related_goods_id = Column(Integer, nullable=False, index=True)
