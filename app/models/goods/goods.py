from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime
from app.config.setting import PAGESIZE,current_page

from app.models.shop.category import Category
from app.models.shop.brand import Brand
from app.models.shop.attribute_category import Attribute_category
import hashlib, time, random
class Goods(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer,index=True,nullable=False,default='0')
    goods_sn = Column(String(255),index=True,nullable=False,default='',)
    name = Column(String(255),nullable=False,default='')
    brand_id = Column(Integer,index=True,nullable=False,default='0')
    goods_num = Column(Integer,index=True,nullable=False,default='0')
    keywords = Column(String(255),nullable=False,default='')
    goods_brief = Column(String(255),nullable=False,default='')
    goods_desc = Column(Text)
    is_on_sale = Column(Integer,nullable=False,default='0')
    sort_order = Column(Integer,index=True,nullable=False,default='100')
    is_delete = Column(Integer,nullable=False,default='0')
    attribute_category = Column(Integer,index=True,nullable=False,default='0')
    counter_price = Column(DECIMAL(10,2),nullable=False,default='0.00')#'专柜价格'
    extra_price = Column(DECIMAL(10,2),nullable=False,default='0.00')# '附加价格'
    is_new = Column(Integer,nullable=False,default='0')
    goods_unit = Column(String(255),nullable=False,default='')# 单位
    primary_pic_url = Column(String(255),nullable=False,default='')# 主图
    list_pic_url = Column(String(255),nullable=False,default='')# 列表图
    retail_price = Column(DECIMAL(10,2),nullable=False,default='0.00') #零售价格
    sell_volume = Column(Integer,nullable=False,default='0')#销售量
    primary_product_id = Column(Integer,nullable=False,default='0') #主图　product_id
    unit_price = Column(DECIMAL(10,2),nullable=False,default='0.00') # 单位价格，单价'
    promotion_desc =  Column(String(255),nullable=False,default='')
    promotion_tag = Column(String(255),nullable=False,default='')
    app_exclusive_price = Column(DECIMAL(10,2),nullable=False,default='0.00')#'APP专享价',
    is_app_exclusive = Column(Integer,nullable=False,default='0') #'是否是APP专属',
    is_limited = Column(Integer,nullable=False,default='0')
    is_hot = Column(Integer,nullable=False,default='0')

    @classmethod
    def generate_order_sn(self):
        m = hashlib.md5()
        sn = None
        while True:
            str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
            m.update(str.encode("utf-8"))
            sn = m.hexdigest()
            if not self.query.filter_by(goods_sn=sn).first():
                break
        return sn

    @classmethod
    def get_info(cls,item):
        info = {
            'id' :item.id,
            'category_id':item.get_cate,
            'goods_sn':item.goods_sn,
            'name':item.name,
            'brand_id':item.get_brand,
            'goods_num':item.goods_num,
            'keywords':item.keywords,
            'goods_brief':item.goods_brief,
            'goods_desc':item.goods_desc,
            'is_on_sale':item.is_on_sale,
            'sort_order':item.sort_order,
            'is_delete':item.is_delete,
            'attribute_category':item.get_attr_cate,
            'counter_price':str(item.counter_price),
            'extra_price':str(item.extra_price),
            'is_new':item.is_new,
            'goods_unit':item.goods_unit,
            'primary_pic_url':item.primary_pic_url,
            'list_pic_url':item.list_pic_url,
            'retail_price':str(item.retail_price),
            'sell_volume':item.sell_volume,
            'primary_product_id':item.primary_product_id,
            'unit_price':str(item.unit_price),
            'promotion_desc':item.promotion_desc,
            'promotion_tag':item.promotion_tag,
            'app_exclusive_price':str(item.app_exclusive_price),
            'is_limited':item.is_limited,
            'is_hot':item.is_hot
        }
        return info

    @property
    def get_cate(cls):
        cate = Category.query.filter_by(id = cls.category_id,delete_time=None).first()
        if cate is None:
            return '暂无分类'
        return cate.name
    
    @property
    def get_brand(cls):
        brand = Brand.query.filter_by(id = cls.brand_id,delete_time=None).first()
        if brand is None:
            return '暂无品牌'
        return brand.name
    
    @property
    def get_attr_cate(cls):
        attr_cate = Attribute_category.query.filter_by(id = cls.attribute_category,delete_time=None).first()
        if attr_cate is None:
            return '暂无系列'
        return attr_cate.name

    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return  info
        
    @classmethod
    def get_all(cls,params=None):
        goods = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
            goods = goods.filter_by(delete_time=None).limit(size).offset((int(page) - 1) * size).all()
        else:
            goods = goods.filter_by(delete_time=None).all()
        if not goods:
            return None
        items = []
        for item in goods:
            info = cls.get_info(item)
            items.append(info)
        return items
    @classmethod
    def search_by_name(cls,q,params=None):
        goods = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
            goods = goods.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).limit(size).offset((int(page) - 1) * size).all()
        else:
            goods =  goods.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).all()
        if not goods:
            return None
        items = []
        for item in goods:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls,form):
        goods = cls.query.filter_by(name = form.name.data,delete_time=None).first()
        if goods is not None :
            return False

        item = cls.create(
            category_id = form.category_id.data if form.category_id.data else '0',
            goods_sn = cls.generate_order_sn(),
            name = form.name.data if form.name.data else '',
            brand_id = form.brand_id.data if form.brand_id.data else '0',
            goods_num = form.goods_num.data if form.goods_num.data else '0',
            keywords = form.keywords.data if form.keywords.data else '',
            goods_brief = form.goods_brief.data if form.goods_brief.data else '',
            goods_desc = form.goods_desc.data if form.goods_desc.data else '',
            is_on_sale = form.is_on_sale.data if form.is_on_sale.data else '0',
            sort_order = form.sort_order.data if form.sort_order.data else '100',
            is_delete = form.is_delete.data if form.is_delete.data else '0',
            attribute_category = form.attribute_category.data if form.attribute_category.data else '0',
            counter_price = form.counter_price.data if form.counter_price.data else '0.00',
            extra_price = form.extra_price.data if form.extra_price.data else '0.00',
            is_new = form.is_new.data if form.is_new.data else '0',
            goods_unit = form.goods_unit.data if form.goods_unit.data else '',
            primary_pic_url = form.primary_pic_url.data if form.primary_pic_url.data else '',
            list_pic_url = form.list_pic_url.data if form.list_pic_url.data else '',
            retail_price = form.retail_price.data if form.retail_price.data else '0.00',
            sell_volume = form.sell_volume.data if form.sell_volume.data else '0',
            primary_product_id = form.primary_product_id.data if form.primary_product_id.data else '0',
            unit_price = form.unit_price.data if form.unit_price.data else '0.00',
            promotion_desc = form.promotion_desc.data if form.promotion_desc.data else '',
            promotion_tag = form.promotion_tag.data if form.promotion_tag.data else '',
            app_exclusive_price = form.form.app_exclusive_price.data if form.app_exclusive_price.data else '0.00',
            is_limited = form.is_limited.data if form.is_limited.data else '0',
            is_hot = form.is_hot.data if form.is_hot.data else '0',
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def edit(cls, id,form):
        goods = cls.query.filter_by(id = id,delete_time=None).first()
        if goods is None:
            return False
        
        item = goods.update(
            id = id,
            category_id = form.category_id.data if form.category_id.data else '0',
            name = form.name.data if form.name.data else '',
            brand_id = form.brand_id.data if form.brand_id.data else '0',
            goods_num = form.goods_num.data if form.goods_num.data else '0',
            keywords = form.keywords.data if form.keywords.data else '',
            goods_brief = form.goods_brief.data if form.goods_brief.data else '',
            goods_desc = form.goods_desc.data if form.goods_desc.data else '',
            is_on_sale = form.is_on_sale.data if form.is_on_sale.data else '0',
            sort_order = form.sort_order.data if form.sort_order.data else '100',
            is_delete = form.is_delete.data if form.is_delete.data else '0',
            attribute_category = form.attribute_category.data if form.attribute_category.data else '0',
            counter_price = form.counter_price.data if form.counter_price.data else '0.00',
            extra_price = form.extra_price.data if form.extra_price.data else '0.00',
            is_new = form.is_new.data if form.is_new.data else '0',
            goods_unit = form.goods_unit.data if form.goods_unit.data else '',
            primary_pic_url = form.primary_pic_url.data if form.primary_pic_url.data else '',
            list_pic_url = form.list_pic_url.data if form.list_pic_url.data else '',
            retail_price = form.retail_price.data if form.retail_price.data else '0.00',
            sell_volume = form.sell_volume.data if form.sell_volume.data else '0',
            primary_product_id = form.primary_product_id.data if form.primary_product_id.data else '0',
            unit_price = form.unit_price.data if form.unit_price.data else '0.00',
            promotion_desc = form.promotion_desc.data if form.promotion_desc.data else '',
            promotion_tag = form.promotion_tag.data if form.promotion_tag.data else '',
            app_exclusive_price = form.form.app_exclusive_price.data if form.app_exclusive_price.data else '0.00',
            is_limited = form.is_limited.data if form.is_limited.data else '0',
            is_hot = form.is_hot.data if form.is_hot.data else '0',
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def remove(cls,id):
        goods = cls.query.filter_by(id = id,delete_time=None).first()
        if goods is None:
            return False
        item = goods.delete(commit=True)
        return True

