from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class Goods(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer,ForeignKey('category.id',onupdate='CASCADE'),nullable=False,default='0')
    goods_sn = Column(String(255),Index=True,nullable=False,default='')
    name = Column(String(255),nullable=False,default='')
    brand_id = Column(Integer,ForeignKey('brand.id',onupdate='CASCADE'),nullable=False,default='0')
    goods_num = Column(Integer,Index=True,nullable=False,default='0')
    keywords = Column(String(255),nullable=False,default='')
    goods_brief = Column(String(255),nullable=False,default='')
    goods_desc = Column(Text)
    is_on_sale = Column(Integer,nullable=False,default='0')
    sort_order = Column(Integer,Index=True,nullable=False,default='100')
    is_delete = Column(Integer,nullable=False,default='0')
    attribute_category = Column(Integer,ForeignKey('attribute_category.id',onupdate='CASCADE'),nullable=False,default='0')
    counter_price = Column(DECIMAL(10,2),nullable=False,default='0.00')#'专柜价格'
    extra_price = Column(DECIMAL(10,2),nullable=False,default='0.00')# '附加价格'
    is_new = Column(Integer,nullable=False,default='0')
    goods_unit = Column(String(255),nullable=False,default='')# 单位
    primary_pic_url = Column(String(255),nullable=False,default='')# 主图
    list_pic_url = Column(String(255),nullable=False,default='')# 列表图
    retail_price = Column(DECIMAL(10,2),nullable=False,default='0.00') #零售价格
    sell_volume = Column(Integer,nullable=False,default='0')#销售量
    primary_product_id = Column(Integer,nullable=False,default='0') #主图　product_id
    unit_price = Column(DECIMAL(10,2),nullable=False,default='0.0.') # 单位价格，单价'
    promotion_desc =  Column(String(255),nullable=False,default='')
    promotion_tag = Column(String(255),nullable=False,default='')
    app_exclusive_price = Column(DECIMAL(10,2),nullable=False,default='0.0.')#'APP专享价',
    is_app_exclusive = Column(Integer,nullable=False,default='0') #'是否是APP专属',
    is_limited = Column(Integer,nullable=False,default='0')
    is_hot = Column(Integer,nullable=False,default='0')
