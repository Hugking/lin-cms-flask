
"""
    :copyright: Â© 2019 by the wkaanig.
    :license: MIT, see LICENSE for more details.
"""
import hashlib
import time
import random
from ..model import *
from flask import current_app as app


class Goods(Goods):
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
    def get_info(cls,item,type=False):
        info = {
            'id' :item.id,
            'category_id':item.get_cate if type else item.category_id,
            'goods_sn':item.goods_sn,
            'name':item.name,
            'brand_id':item.get_brand if type else item.brand_id,
            'goods_num':item.goods_num,
            'keywords':item.keywords,
            'goods_brief':item.goods_brief,
            'goods_desc':item.goods_desc,
            'is_on_sale':item.is_on_sale,
            'sort_order':item.sort_order,
            'is_delete':item.is_delete,
            'attribute_category':item.get_attr_cate if type else item.attribute_category,
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
        attr_cate = AttributeCategory.query.filter_by(id = cls.attribute_category,delete_time=None).first()
        if attr_cate is None:
            return '暂无系列'
        return attr_cate.name

    @classmethod
    def get_detail(cls, id, type=False):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item,type)
        return  info
        
    @classmethod
    def get_all(cls,params=None, type=False):
        goods = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            goods = goods.filter_by(delete_time=None).order_by(cls.id.desc()).limit(size).offset((int(page) - 1) * size).all()
        else:
            goods = goods.filter_by(delete_time=None).order_by(cls.id.desc()).all()
        if not goods:
            return None
        items = []
        for item in goods:
            info = cls.get_info(item,type)
            items.append(info)
        return items
    
    @classmethod
    def get_count(cls):
        item = cls.query.filter_by(delete_time=None).count()
        return  item
        

    @classmethod
    def search_by_name(cls,q,params=None,type=False):
        goods = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            goods = goods.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).order_by(cls.id.desc()).limit(size).offset((int(page) - 1) * size).all()
        else:
            goods =  goods.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).order_by(cls.id.desc()).all()
        if not goods:
            return None
        items = []
        for item in goods:
            info = cls.get_info(item,type)
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
            app_exclusive_price = form.app_exclusive_price.data if form.app_exclusive_price.data else '0.00',
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
class GoodsAttribute(GoodsAttribute):
    @classmethod
    def get_info(cls,item,type=False):
        info = {
            'id' :item.id,
            'attribute_id':item.get_attr if type else item.attribute_id,
            'goods_id':item.get_goods if type else item.goods_id,
            'values':item.values,
        }
        return info

    @property
    def get_attr(cls):
        attribute = Attribute.query.filter_by(id = cls.attribute_id,delete_time=None).first()
        if attribute is None:
            return '无匹配'
        return attribute.name

    @property
    def get_goods(cls):
        goods = Goods.query.filter_by(id = cls.goods_id,delete_time=None).first()
        if goods is None:
            return '商品不存在'
        return goods.name


    @classmethod
    def get_detail(cls, id,type=False):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item,type)
        return  info
        
    @classmethod
    def get_all(cls,params=None,type=False):
        goods_attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            goods_attribute = goods_attribute.filter(cls.delete_time == None).order_by(cls.goods_id.desc(),cls.attribute_id.desc())
            goods_attribute = goods_attribute.limit(size).offset((int(page) - 1) * size).all()
        else:
            goods_attribute = goods_attribute.filter_by(delete_time=None).order_by(cls.goods_id.desc(),cls.attribute_id.desc()).all()
        if not goods_attribute:
            return None
        items = []
        for item in goods_attribute:
            info = cls.get_info(item,type)
            items.append(info)
        return items
    
    @classmethod
    def search_by_keywords(cls,params=None,type=False):
        goods_attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            attribute_id = int(params['attribute_id']) if 'attribute_id' in params else None
            goods_id = int(params['goods_id']) if 'goods_id' in params else None
            if attribute_id is not None:
                goods_attribute = goods_attribute.filter(cls.attribute_id == attribute_id)
            if goods_id is not None:
                goods_attribute = goods_attribute.filter(cls.goods_id == goods_id)
            goods_attribute = goods_attribute.filter(cls.delete_time == None).order_by(cls.goods_id.desc(),cls.attribute_id.desc())
            goods_attribute = goods_attribute.limit(size).offset((int(page) - 1) * size).all()
            if not goods_attribute:
                return None
            items = []
            for item in goods_attribute:
                info = cls.get_info(item,type)
                items.append(info)
            return items
        return None
    

    @classmethod
    def new(cls,form):
        goods = Goods.query.filter_by(id = int(form.goods_id.data),delete_time=None).first()
        if goods is None :
            return False

        attribute = Attribute.query.filter_by(id = int(form.attribute_id.data),delete_time=None).first()
        if attribute is None:
            return False
        
        old_goods_attr = cls.query.filter_by(attribute_id = int(form.attribute_id.data),goods_id = int(form.goods_id.data),delete_time=None).first()
        if old_goods_attr is not None:
            return -1

        item = cls.create(
            attribute_id = int(form.attribute_id.data) if form.attribute_id.data else '0',
            goods_id= int(form.goods_id.data) if form.goods_id.data else '0',
            values = form.values.data if form.values.data else '',
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def edit(cls, id,form):
        goods = Goods.query.filter_by(id = int(form.goods_id.data),delete_time=None).first()
        if goods is None :
            return False

        attribute = Attribute.query.filter_by(id = int(form.attribute_id.data),delete_time=None).first()
        if attribute is None:
            return False

        goods_attribute = cls.query.filter_by(id = id,delete_time=None).first()
        if goods_attribute is None:
            return False

        old_goods_attr = cls.query.filter_by(attribute_id = int(form.attribute_id.data),goods_id = int(form.goods_id.data),delete_time=None).first()
        if old_goods_attr is not None:
            return -1
        
        item = goods_attribute.update(
            id = id,
            attribute_id = int(form.attribute_id.data) if form.attribute_id.data else '0',
            goods_id= int(form.goods_id.data) if form.goods_id.data else '0',
            values = form.values.data if form.values.data else '',
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def remove(cls,id):
        goods_attribute = cls.query.filter_by(id = id,delete_time=None).first()
        if goods_attribute is None:
            return False
        goods_attribute.delete(commit=True)
        return True
class Attribute(Attribute):
    @classmethod
    def get_info(cls,item,type=False):
        info = {
            'id' :item.id,
            'attribute_category_id':item.get_attr_cate if type else item.attribute_category_id,
            'name':item.name,
            'input_type':item.input_type,
            'values':item.values,
            'sort_order':item.sort_order
        }
        return info

    @property
    def get_attr_cate(cls):
        attribute_category = AttributeCategory.query.filter_by(id = cls.attribute_category_id,delete_time=None).first()
        if attribute_category is None:
            return 'ć ĺšé'
        return  attribute_category.name


    @classmethod
    def get_detail(cls, id,type=False):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item,type)
        return  info
        
    @classmethod
    def get_all(cls,params=None,type=False):
        attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            attribute = attribute.filter_by(delete_time=None).limit(size).offset((int(page) - 1) * size).all()
        else:
            attribute = attribute.filter_by(delete_time=None).all()
        if not attribute:
            return None
        items = []
        for item in attribute:
            info = cls.get_info(item,type)
            items.append(info)
        return items
    
    @classmethod
    def search_by_name(cls,q,params=None,type=False):
        attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            attribute = attribute.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).limit(size).offset((int(page) - 1) * size).all()
        else:
            attribute =  attribute.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).all()
        if not attribute:
            return None
        items = []
        for item in attribute:
            info = cls.get_info(item,type)
            items.append(info)
        return items

    @classmethod
    def new(cls,form):
        attribute = cls.query.filter_by(name = form.name.data,delete_time=None).first()
        if attribute is not None :
            return False

        attribute_category = AttributeCategory.query.filter_by(id = int(form.attribute_category_id.data),delete_time=None).first()
        if attribute_category is None:
            return False

        input_type = form.input_type.data if form.input_type.data else '1'
        values = form.values.data if form.values.data else ''
        sort_order = form.sort_order.data if form.sort_order.data else '0'
        
        item = cls.create(
            name = form.name.data,
            attribute_category_id = int(form.attribute_category_id.data),
            input_type = input_type,
            values = values,
            sort_order = sort_order,
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def edit(cls, id,form):
        attribute = cls.query.filter_by(id = id,delete_time=None).first()
        if attribute is None:
            return False
        
        attribute_category = AttributeCategory.query.filter_by(id = int(form.attribute_category_id.data),delete_time=None).first()
        if attribute_category is None:
            return False

        input_type = form.input_type.data if form.input_type.data else '1'
        values = form.values.data if form.values.data else ''
        sort_order = form.sort_order.data if form.sort_order.data else '0'
        
        item = attribute.update(
            id = id,
            name = form.name.data,
            attribute_category_id = int(form.attribute_category_id.data),
            input_type = input_type,
            values = values,
            sort_order = sort_order,
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def remove(cls,id):
        attribute = cls.query.filter_by(id = id,delete_time=None).first()
        if attribute is None:
            return False
        attribute.delete(commit=True)
        return True
class AttributeCategory(AttributeCategory):
    @classmethod
    def get_info(cls,item):
        info = {
            'id' :item.id,
            'name':item.name
        }
        return info


    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return info
        
    @classmethod
    def get_all(cls,params=None):
        attribute_category = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            attribute_category = attribute_category.filter_by(delete_time=None).limit(size).offset((int(page) - 1) * size).all()
        else:
            attribute_category = attribute_category.filter_by(delete_time=None).all()
        if not attribute_category:
            return None
        items = []
        for item in attribute_category:
            info = cls.get_info(item)
            items.append(info)
        return items
    
    @classmethod
    def search_by_name(cls,q,params=None):
        attribute_category = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            attribute_category = attribute_category.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).limit(size).offset((int(page) - 1) * size).all()
        else:
            attribute_category =  attribute_category.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).all()
        if not attribute_category:
            return None
        items = []
        for item in attribute_category:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls,form):
        attribute_category = cls.query.filter_by(name = form.name.data,delete_time=None).first()
        if attribute_category is not None:
            return False

        item = cls.create(
            name = form.name.data,
            commit = True
        )
        info = cls.get_info(item)
        return info
    
    @classmethod
    def edit(cls, id,form):
        attribute_category = cls.query.filter_by(id = id,delete_time=None).first()
        if attribute_category is None:
            return False

        item = attribute_category.update(
            id = id,
            name = form.name.data,
            commit = True
        )
        info = cls.get_info(item)
        return info
    
    @classmethod
    def remove(cls,id):
        attribute_category = cls.query.filter_by(id = id,delete_time=None).first()
        if attribute_category is None:
            return False
        attribute_category.delete(commit=True)
        return True
class Brand(Brand):
    @classmethod
    def get_info(cls,item):
        info = {
            'id' :item.id,
            'name':item.name,
            'list_pic_url':item.list_pic_url,
            'simple_desc':item.simple_desc,
            'pic_url':item.pic_url,
            'sort_order':item.sort_order,
            'is_show':item.is_show,
            'floor_price':str(item.floor_price),
            'app_list_pic_url':item.app_list_pic_url,
            'is_new':item.is_new,
            'new_pic_url':item.new_pic_url,
            'new_sort_order':item.new_sort_order
        }
        return info

    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return  info
        
    @classmethod
    def get_all(cls,params=None):
        brand = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            brand = brand.filter_by(delete_time=None).limit(size).offset((int(page) - 1) * size).all()
        else:
            brand = brand.filter_by(delete_time=None).all()
        if not brand:
            return None
        items = []
        for item in brand:
            info = cls.get_info(item)
            items.append(info)
        return items
    @classmethod
    def search_by_name(cls,q,params=None):
        brand = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            brand = brand.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).limit(size).offset((int(page) - 1) * size).all()
        else:
            brand =  brand.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).all()
        if not brand:
            return None
        items = []
        for item in brand:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls,form):
        brand = cls.query.filter_by(name = form.name.data,delete_time=None).first()
        if brand is not None :
            return False

        item = cls.create(
            name = form.name.data if form.name.data else '',
            list_pic_url = form.list_pic_url.data if form.list_pic_url.data else '',
            simple_desc = form.simple_desc.data if form.simple_desc.data else '',
            pic_url = form.pic_url.data if form.pic_url.data else '',
            sort_order = form.sort_order.data if  form.sort_order.data else '50',
            is_show = form.is_show.data if form.is_show.data else '1',
            floor_price = form.floor_price.data if form.floor_price.data else '0.00',
            app_list_pic_url = form.app_list_pic_url.data if form.app_list_pic_url.data else '',
            is_new = form.is_new.data if form.is_new.data else '0',
            new_pic_url = form.new_pic_url.data if form.new_pic_url.data else '',
            new_sort_order = form.new_sort_order.data if form.new_sort_order.data else '100',
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def edit(cls, id,form):
        brand = cls.query.filter_by(id = id,delete_time=None).first()
        if brand is None:
            return False
        
        item = brand.update(
            id = id,
            name = form.name.data if form.name.data else '',
            list_pic_url = form.list_pic_url.data if form.list_pic_url.data else '',
            simple_desc = form.simple_desc.data if form.simple_desc.data else '',
            pic_url = form.pic_url.data if form.pic_url.data else '',
            sort_order = form.sort_order.data if  form.sort_order.data else '50',
            is_show = form.is_show.data if form.is_show.data else '1',
            floor_price = form.floor_price.data if form.floor_price.data else '0.00',
            app_list_pic_url = form.app_list_pic_url.data if form.app_list_pic_url.data else '',
            is_new = form.is_new.data if form.is_new.data else '0',
            new_pic_url = form.new_pic_url.data if form.new_pic_url.data else '',
            new_sort_order = form.new_sort_order.data if form.new_sort_order.data else '100',
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def remove(cls,id):
        brand = cls.query.filter_by(id = id,delete_time=None).first()
        if brand is None:
            return False
        item = brand.delete(commit=True)
        return True
class Category(Category):
    @classmethod
    def get_info(cls,item):
        info = {
            'id' :item.id,
            'name':item.name,
            'keywords':item.keywords,
            'front_desc':item.front_desc,
            'parent_id':item.parent_id,
            'sort_order':item.sort_order,
            'show_index':item.show_index,
            'banner_url':item.banner_url,
            'icon_url':item.icon_url,
            'img_url':item.img_url,
            'wap_banner_url':item.wap_banner_url,
            'level':item.level,
            'type':item.type
            }
        return info

    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return info
        
    @classmethod
    def get_all(cls,params=None):
        category = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            category = category.filter_by(delete_time=None).limit(size).offset((int(page) - 1) * size).all()
        else:
            category = category.filter_by(delete_time=None).all()
        if not category:
            return None
        items = []
        for item in category:
            info = cls.get_info(item)
            items.append(info)
        return items
    
    @classmethod
    def search_by_name(cls,q,params=None):
        category = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            category = category.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).limit(size).offset((int(page) - 1) * size).all()
        else:
            category =  category.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).all()
        if not category:
            return None
        items = []
        for item in category:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls,form):
        category = cls.query.filter_by(name = form.name.data,delete_time=None).first()
        if category is not None:
            return False

        front_name = form.front_name.data if form.front_name.data else '',
        front_desc = form.front_desc.data if form.front_desc.data else '',
        parent_id = form.parent_id.data if form.parent_id.data else '0',
        sort_order = form.sort_order.data if form.sort_order.data else '50',
        show_index = form.show_index.data if form.show_index.data else '0',
        banner_url = form.banner_url.data if form.banner_url.data else '',
        icon_url = form.icon_url.data if form.icon_url.data else '',
        img_url = form.img_url.data if form.img_url.data else '',
        wap_banner_url = form.wap_banner_url.data if form.wap_banner_url.data else '',
        level = form.level.data if form.level.data else '',
        type = form.type.data if form.type.data else '0',

        item = cls.create(
            name = form.name.data,
            keywords = form.keywords.data,
            front_name = front_name,
            front_desc = front_desc,
            parent_id = parent_id,
            sort_order = sort_order,
            show_index = show_index,
            banner_url = banner_url,
            icon_url = icon_url,
            img_url = img_url,
            wap_banner_url = wap_banner_url,
            level = level,
            type = type,
            commit = True
        )
        info = cls.get_info(item)
        return info
    
    @classmethod
    def edit(cls, id,form):
        category = Category.query.filter_by(id = id,delete_time=None).first()
        if category is None:
            return False
        
        front_name = form.front_name.data if form.front_name.data else '',
        front_desc = form.front_desc.data if form.front_desc.data else '',
        parent_id = form.parent_id.data if form.parent_id.data else '0',
        sort_order = form.sort_order.data if form.sort_order.data else '50',
        show_index = form.show_index.data if form.show_index.data else '0',
        banner_url = form.banner_url.data if form.banner_url.data else '',
        icon_url = form.icon_url.data if form.icon_url.data else '',
        img_url = form.img_url.data if form.img_url.data else '',
        wap_banner_url = form.wap_banner_url.data if form.wap_banner_url.data else '',
        level = form.level.data if form.level.data else '',
        type = form.type.data if form.type.data else '0',

        item = category.update(
            id = id,
            name = form.name.data,
            keywords = form.keywords.data,
            front_name = front_name,
            front_desc = front_desc,
            parent_id = parent_id,
            sort_order = sort_order,
            show_index = show_index,
            banner_url = banner_url,
            icon_url = icon_url,
            img_url = img_url,
            wap_banner_url = wap_banner_url,
            level = level,
            type = type,
            commit = True
        )
        info = cls.get_info(item)
        return info
    
    @classmethod
    def remove(cls,id):
        category = Category.query.filter_by(id = id,delete_time=None).first()
        if category is None:
            return False
        category.delete(commit=True)
        return True
class Keywords(Keywords):
    @classmethod
    def get_info(cls,item):
        info = {
            'id' :item.id,
            'is_hot':item.is_hot,
            'is_default':item.is_default,
            'is_show':item.is_show,
            'scheme_url':item.scheme_url,
            'sort_order':item.sort_order,
            'type':item.type
        }
        return info

    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return  info
        
    @classmethod
    def get_all(cls,params=None):
        keywords = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else app.config['current_page']
            size = params['size'] if 'size' in params else app.config['PAGESIZE']
            keywords = keywords.filter_by(delete_time=None).limit(size).offset((int(page) - 1) * size).all()
        else:
            keywords = keywords.filter_by(delete_time=None).all()
        if not keywords:
            return None
        items = []
        for item in keywords:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls,form):
        item = cls.create(
            is_hot = form.is_hot.data if form.is_hot.data else '0',
            is_default = form.is_default.data if form.is_default.data else '0',
            is_show = form.is_show.data if form.is_show.data else '1',
            scheme_url = form.scheme_url.data if form.scheme_url.data else '0',
            sort_order = form.sort_order.data if form.sort_order.data else '100',
            type  = form.type.data if form.type.data else '0',
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def edit(cls, id,form):
        keywords = cls.query.filter_by(id = id,delete_time=None).first()
        if keywords is None:
            return False
        
        item = keywords.update(
            id = id,
            is_hot = form.is_hot.data if form.is_hot.data else '0',
            is_default = form.is_default.data if form.is_default.data else '0',
            is_show = form.is_show.data if form.is_show.data else '1',
            scheme_url = form.scheme_url.data if form.scheme_url.data else '0',
            sort_order = form.sort_order.data if form.sort_order.data else '100',
            type  = form.type.data if form.type.data else '0',
            commit = True
        )
        info = cls.get_info(item)
        return  info
    
    @classmethod
    def remove(cls,id):
        keywords = cls.query.filter_by(id = id,delete_time=None).first()
        if keywords is None:
            return False
        item = keywords.delete(commit=True)
        return True
