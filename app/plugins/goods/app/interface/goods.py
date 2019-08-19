"""
    :copyright: Â© 2019 by the wkaanig.
    :license: MIT, see LICENSE for more details.
"""
import hashlib
import time
import json
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
    def get_info(cls, item, mini=False):
        info = {
            'id': item.id,
            'category_id': item.get_cate if mini else [v for v in item.category_id.split('|')],
            'goods_sn': item.goods_sn,
            'name': item.name,
            'brand_id': item.get_brand if mini else item.brand_id,
            'goods_num': item.goods_num,
            'keywords': item.keywords,
            'goods_brief': item.goods_brief,
            'goods_desc': item.goods_desc,
            'sort_order': item.sort_order,
            'attribute_category': item.get_attr_cate if mini else [v for v in
                                                                   item.attribute_category.split(
                                                                       '|')],
            'counter_price': str(item.counter_price),
            'extra_price': str(item.extra_price),
            'goods_unit': item.goods_unit,
            'primary_pic_url': [] if item.primary_pic_url.split('|') == [
                ""] else item.primary_pic_url.split('|'),
            'list_pic_url': [] if item.list_pic_url.split('|') == [""] else item.list_pic_url.split(
                '|'),
            'retail_price': str(item.retail_price),
            'sell_volume': item.sell_volume,
            'primary_product_id': item.primary_product_id,
            'unit_price': str(item.unit_price),
            'promotion_desc': item.promotion_desc,
            'promotion_tag': item.promotion_tag,
            'app_exclusive_price': str(item.app_exclusive_price),
            'is_new': True if item.is_new == 1 else False,
            'is_on_sale': True if item.is_on_sale == 1 else False,
            'is_delete': True if item.is_delete == 1 else False,
            'is_limited': True if item.is_limited == 1 else False,
            'is_hot': True if item.is_hot == 1 else False
        }
        return info

    @property
    def get_cate(cls):
        cate = Category.query.filter_by(id=cls.category_id, delete_time=None).first()
        if cate is None:
            return '暂无分类'
        return cate.name

    @property
    def get_brand(cls):
        brand = Brand.query.filter_by(id=cls.brand_id, delete_time=None).first()
        if brand is None:
            return '暂无品牌'
        return brand.name

    @property
    def get_attr_cate(cls):
        attr_cate = AttributeCategory.query.filter_by(id=cls.attribute_category,
                                                      delete_time=None).first()
        if attr_cate is None:
            return '暂无系列'
        return attr_cate.name

    @classmethod
    def get_detail(cls, id, mini=False):
        item = cls.query.filter_by(id=id, delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item, mini)
        return info

    @classmethod
    def get_all(cls, params=None, mini=False):
        goods = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            goods = goods.filter_by(delete_time=None).order_by(cls.id.desc()).limit(size).offset(
                (int(page) - 1) * size).all()
        else:
            goods = goods.filter_by(delete_time=None).order_by(cls.id.desc()).all()
        if not goods:
            return None
        items = []
        for item in goods:
            info = cls.get_info(item, mini)
            items.append(info)
        return items

    @classmethod
    def get_count(cls):
        item = cls.query.filter_by(delete_time=None).count()
        return item

    @classmethod
    def search_by_keywords(cls, form, mini=False):
        goods = cls.query
        page = form.page.data if form.page.data else 1
        size = form.size.data if form.size.data else 20
        if form.name.data:
            goods = goods.filter(cls.name.like('%' + form.name.data + '%'))
        if form.brand.data:
            goods = goods.filter_by(brand=form.brand.data)
        if form.category_id.data:
            goods = goods.filter(or_(cls.category_id.like('%|' + form.category_id.data + '|%'),
                                     cls.category_id.like('%|' + form.category_id.data), \
                                     cls.category_id.like(form.category_id.data + '|%'),
                                     cls.category_id.like(form.category_id.data)))

        goods = goods.filter(cls.delete_time == None).order_by(cls.id.desc()).limit(size).offset(
            (int(page) - 1) * size).all()

        if not goods:
            return None
        items = []
        for item in goods:
            info = cls.get_info(item, mini)
            items.append(info)
        return items

    @classmethod
    def new(cls, form):
        goods = cls.query.filter_by(name=form.name.data, delete_time=None).first()
        if goods is not None:
            return False

        category_id = '|'.join('%s' % id for id in form.category_id.data) if type(
            form.category_id.data) == list else form.category_id.data
        attribute_category = '|'.join('%s' % id for id in form.attribute_category.data) if type(
            form.attribute_category.data) == list else form.attribute_category.data
        list_pic_url = '|'.join('%s' % id for id in form.list_pic_url.data) if type(
            form.list_pic_url.data) == list else form.list_pic_url.data
        primary_pic_url = '|'.join('%s' % id for id in form.primary_pic_url.data) if type(
            form.primary_pic_url.data) == list else form.primary_pic_url.data

        item = cls.create(
            category_id=category_id if form.category_id.data else '',
            goods_sn=cls.generate_order_sn(),
            name=form.name.data if form.name.data else '',
            brand_id=form.brand_id.data if form.brand_id.data else '0',
            goods_num=form.goods_num.data if form.goods_num.data else '0',
            goods_brief=form.goods_brief.data if form.goods_brief.data else '',
            goods_desc=form.goods_desc.data if form.goods_desc.data else '',
            attribute_category=attribute_category if form.attribute_category.data else '',
            unit_price=form.unit_price.data if form.unit_price.data else '0.00',
            goods_unit=form.goods_unit.data if form.goods_unit.data else '',
            primary_pic_url=primary_pic_url,
            list_pic_url=list_pic_url if form.list_pic_url.data else '',
            retail_price=form.retail_price.data if form.retail_price.data else '0.00',
            primary_product_id=form.primary_product_id.data if form.primary_product_id.data else
            '0',
            counter_price=form.counter_price.data if form.counter_price.data else '0.00',
            extra_price=form.extra_price.data if form.extra_price.data else '0.00',
            sort_order=form.sort_order.data if form.sort_order.data else '100',
            is_delete=form.is_delete.data if form.is_delete.data else '0',
            app_exclusive_price=form.app_exclusive_price.data if form.app_exclusive_price.data
            else '0.00',
            keywords=form.keywords.data if form.keywords.data else '',
            sell_volume=form.sell_volume.data if form.sell_volume.data else '0',
            promotion_desc=form.promotion_desc.data if form.promotion_desc.data else '',
            promotion_tag=form.promotion_tag.data if form.promotion_tag.data else '',
            is_new='1' if form.is_new.data is True else '0',
            is_on_sale='1' if form.is_on_sale.data is True else '0',
            is_limited='1' if form.is_limited.data is True else '0',
            is_hot='1' if form.is_hot.data is True else '0',
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def edit(cls, id, form):
        goods = cls.query.filter_by(id=id, delete_time=None).first()
        if goods is None:
            return False

        category_id = '|'.join('%s' % id for id in form.category_id.data) if type(
            form.category_id.data) == list else form.category_id.data
        attribute_category = '|'.join('%s' % id for id in form.attribute_category.data) if type(
            form.attribute_category.data) == list else form.attribute_category.data
        list_pic_url = '|'.join('%s' % id for id in form.list_pic_url.data) if type(
            form.list_pic_url.data) == list else form.list_pic_url.data
        primary_pic_url = '|'.join('%s' % id for id in form.primary_pic_url.data) if type(
            form.primary_pic_url.data) == list else form.primary_pic_url.data

        item = goods.update(
            id=id,
            category_id=category_id if form.category_id.data else '',
            goods_sn=form.goods_sn.data if form.goods_sn.data else '',
            name=form.name.data if form.name.data else '',
            brand_id=form.brand_id.data if form.brand_id.data else '0',
            goods_num=form.goods_num.data if form.goods_num.data else '0',
            goods_brief=form.goods_brief.data if form.goods_brief.data else '',
            goods_desc=form.goods_desc.data if form.goods_desc.data else '',
            attribute_category=attribute_category if form.attribute_category.data else '',
            unit_price=form.unit_price.data if form.unit_price.data else '0.00',
            goods_unit=form.goods_unit.data if form.goods_unit.data else '',
            primary_pic_url=primary_pic_url,
            list_pic_url=list_pic_url if form.list_pic_url.data else '',
            retail_price=form.retail_price.data if form.retail_price.data else '0.00',
            primary_product_id=form.primary_product_id.data if form.primary_product_id.data else
            '0',
            counter_price=form.counter_price.data if form.counter_price.data else '0.00',
            extra_price=form.extra_price.data if form.extra_price.data else '0.00',
            sort_order=form.sort_order.data if form.sort_order.data else '100',
            is_delete=form.is_delete.data if form.is_delete.data else '0',
            app_exclusive_price=form.app_exclusive_price.data if form.app_exclusive_price.data
            else '0.00',
            keywords=form.keywords.data if form.keywords.data else '',
            sell_volume=form.sell_volume.data if form.sell_volume.data else '0',
            promotion_desc=form.promotion_desc.data if form.promotion_desc.data else '',
            promotion_tag=form.promotion_tag.data if form.promotion_tag.data else '',
            is_new='1' if form.is_new.data is True else '0',
            is_on_sale='1' if form.is_on_sale.data is True else '0',
            is_limited='1' if form.is_limited.data is True else '0',
            is_hot='1' if form.is_hot.data is True else '0',
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def remove(cls, id):
        goods = cls.query.filter_by(id=id, delete_time=None).first()
        if goods is None:
            return False
        item = goods.delete(commit=True)
        return True


class GoodsAttribute(GoodsAttribute):

    @classmethod
    def get_info(cls, item, mini=False):
        info = {
            'id': item.id,
            'attribute_id': item.get_attr,
            'goods_id': item.get_goods if mini else item.goods_id,
            'values': item.values,
        }
        return info

    @property
    def get_attr(cls):
        attribute = Attribute.query.filter_by(id=cls.attribute_id, delete_time=None).first()
        attribute_info = {
            'id': attribute.id if attribute else cls.attribute_id,
            'attribute_category_id': attribute.attribute_category_id if attribute else '0',
            'name': attribute.name if attribute else '无匹配'
        }
        return attribute_info

    @property
    def get_goods(cls):
        goods = Goods.query.filter_by(id=cls.goods_id, delete_time=None).first()
        if goods is None:
            return '商品不存在'
        return goods.name

    @classmethod
    def get_detail(cls, id, mini=False):
        item = cls.query.filter_by(id=id, delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item, mini)
        return info

    @classmethod
    def get_all(cls, params=None, mini=False):
        goods_attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            goods_attribute = goods_attribute.filter(cls.delete_time == None).order_by(
                cls.goods_id.desc(), cls.attribute_id.desc())
            goods_attribute = goods_attribute.limit(size).offset((int(page) - 1) * size).all()
        else:
            goods_attribute = goods_attribute.filter_by(delete_time=None).order_by(
                cls.goods_id.desc(), cls.attribute_id.desc()).all()
        if not goods_attribute:
            return None
        items = []
        for item in goods_attribute:
            info = cls.get_info(item, mini)
            items.append(info)
        return items

    @classmethod
    def search_by_keywords(cls, form, mini=False):
        goods_attribute = cls.query
        page = int(form.page.data) if form.page.data else 1
        size = int(form.size.data) if form.size.data else 20
        if form.attribute_id.data:
            goods_attribute = goods_attribute.filter_by(attribute_id=form.attribute_id.data)
        if form.goods_id.data:
            goods_attribute = goods_attribute.filter_by(goods_id=form.goods_id.data)

        goods_attribute = goods_attribute.filter(cls.delete_time == None).order_by(
            cls.goods_id.desc(), cls.attribute_id.desc())
        goods_attribute = goods_attribute.limit(size).offset((int(page) - 1) * size).all()
        if not goods_attribute:
            return None
        items = []
        for item in goods_attribute:
            info = cls.get_info(item, mini)
            items.append(info)
        return items

    @classmethod
    def new(cls, form):
        goods = Goods.query.filter_by(id=int(form.goods_id.data), delete_time=None).first()
        if goods is None:
            return False

        attribute = Attribute.query.filter_by(id=int(form.attribute_id.data),
                                              delete_time=None).first()
        if attribute is None:
            return False

        old_goods_attr = cls.query.filter_by(attribute_id=int(form.attribute_id.data),
                                             goods_id=int(form.goods_id.data),
                                             delete_time=None).first()
        if old_goods_attr is not None:
            return -1

        item = cls.create(
            attribute_id=int(form.attribute_id.data) if form.attribute_id.data else '0',
            goods_id=int(form.goods_id.data) if form.goods_id.data else '0',
            values=form.values.data if form.values.data else '',
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def edit(cls, id, form):
        goods = Goods.query.filter_by(id=int(form.goods_id.data), delete_time=None).first()
        if goods is None:
            return False

        attribute = Attribute.query.filter_by(id=int(form.attribute_id.data),
                                              delete_time=None).first()
        if attribute is None:
            return False

        goods_attribute = cls.query.filter_by(id=id, delete_time=None).first()
        if goods_attribute is None:
            return False

        old_goods_attr = cls.query.filter_by(attribute_id=int(form.attribute_id.data),
                                             goods_id=int(form.goods_id.data),
                                             delete_time=None).first()
        if old_goods_attr is not None:
            return -1

        item = goods_attribute.update(
            id=id,
            attribute_id=int(form.attribute_id.data) if form.attribute_id.data else '0',
            goods_id=int(form.goods_id.data) if form.goods_id.data else '0',
            values=form.values.data if form.values.data else '',
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def remove(cls, id):
        goods_attribute = cls.query
        goods_attribute = goods_attribute.filter_by(id=id, delete_time=None).first()
        if goods_attribute is None:
            return False
        goods_attribute.delete(commit=True)
        return True


class Attribute(Attribute):
    @classmethod
    def get_info(cls, item, mini=False):
        info = {
            'id': item.id,
            'attribute_category_id': item.get_attr_cate if mini else item.attribute_category_id,
            'name': item.name,
            'input_type': item.input_type,
            'values': item.values,
            'sort_order': item.sort_order
        }
        return info

    @property
    def get_attr_cate(cls):
        attribute_category = AttributeCategory.query.filter_by(id=cls.attribute_category_id,
                                                               delete_time=None).first()
        if attribute_category is None:
            return '无匹配'
        return attribute_category.name

    @classmethod
    def get_detail(cls, id, mini=False):
        item = cls.query.filter_by(id=id, delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item, mini)
        return info

    @classmethod
    def get_all(cls, params=None, mini=False):
        attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            attribute = attribute.filter_by(delete_time=None).order_by(cls.id.desc()).limit(
                size).offset((int(page) - 1) * size).all()
        else:
            attribute = attribute.filter_by(delete_time=None).order_by(cls.id.desc()).limit(
                20).offset(0).all()
        if not attribute:
            return None
        items = []
        for item in attribute:
            info = cls.get_info(item, mini)
            items.append(info)
        return items

    @classmethod
    def search_by_keywords(cls, params=None, mini=False):
        attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            if 'attribute_category_id' in params:
                attribute = attribute.filter_by(
                    attribute_category_id=params['attribute_category_id'])
            attribute = attribute.filter_by(delete_time=None).order_by(cls.id.desc()).limit(
                size).offset((int(page) - 1) * size).all()
        else:
            attribute = attribute.filter_by(delete_time=None).order_by(cls.id.desc()).limit(
                20).offset(0).all()
        if not attribute:
            return None
        items = []
        for item in attribute:
            info = cls.get_info(item, mini)
            items.append(info)
        return items

    @classmethod
    def new(cls, form):
        attribute = cls.query.filter_by(name=form.name.data, delete_time=None).first()
        if attribute is not None:
            return False

        attribute_category = AttributeCategory.query.filter_by(
            id=int(form.attribute_category_id.data), delete_time=None).first()
        if attribute_category is None:
            return False

        input_type = form.input_type.data if form.input_type.data else '1'
        values = form.values.data if form.values.data else ''
        sort_order = form.sort_order.data if form.sort_order.data else '0'

        item = cls.create(
            name=form.name.data,
            attribute_category_id=int(form.attribute_category_id.data),
            input_type=input_type,
            values=values,
            sort_order=sort_order,
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def edit(cls, id, form):
        attribute = cls.query.filter_by(id=id, delete_time=None).first()
        if attribute is None:
            return False

        attribute_category = AttributeCategory.query.filter_by(
            id=int(form.attribute_category_id.data), delete_time=None).first()
        if attribute_category is None:
            return False

        input_type = form.input_type.data if form.input_type.data else '1'
        values = form.values.data if form.values.data else ''
        sort_order = form.sort_order.data if form.sort_order.data else '0'

        item = attribute.update(
            id=id,
            name=form.name.data,
            attribute_category_id=int(form.attribute_category_id.data),
            input_type=input_type,
            values=values,
            sort_order=sort_order,
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def remove(cls, id):
        attribute = cls.query.filter_by(id=id, delete_time=None).first()
        goods_list = Goods.query.filter(
            or_(Goods.attribute_category.like('%|' + id + '|%'),
                Goods.attribute_category.like('%|' + id),
                Goods.attribute_category.like(id + '|%'),
                Goods.attribute_category.like(id))).all()
        for goods in goods_list:
            attr_cate_list = [v for v in goods.attribute_category.split('|')]
            attr_cate_list.remove(str(id))
            attr_cate = '|'.join('%s' % id for id in attr_cate_list)
            goods.update(id=goods.id, attribute_category=attr_cate, commit=True)
            goods_attr_list = GoodsAttribute.query.filter_by(goods_id=goods.id, attribute_id=id,
                                                        delete_time=None).all()
            for goods_attr in goods_attr_list:
                goods_attr.delete(commit=True)
        if attribute is None:
            return False
        attribute.delete(commit=True)
        return True


class AttributeCategory(AttributeCategory):

    @classmethod
    def get_attr_list(cls, id):
        params = {
            "page": 1,
            "size": 100,
            "attribute_category_id": id
        }
        attr_list = Attribute.search_by_keywords(params)
        return attr_list

    @classmethod
    def get_info(cls, item):
        attr_list = cls.get_attr_list(item.id)
        info = {
            'id': item.id,
            'name': item.name,
            'attr_list': attr_list
        }
        return info

    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id=id, delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return info

    @classmethod
    def get_all(cls, params=None):
        attribute_category = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            attribute_category = attribute_category.filter_by(delete_time=None).limit(size).offset(
                (int(page) - 1) * size).all()
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
    def search_by_name(cls, q, params=None):
        attribute_category = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            attribute_category = attribute_category.filter(cls.name.like('%' + q + '%'),
                                                           cls.delete_time == None).limit(
                size).offset((int(page) - 1) * size).all()
        else:
            attribute_category = attribute_category.filter(cls.name.like('%' + q + '%'),
                                                           cls.delete_time == None).all()
        if not attribute_category:
            return None
        items = []
        for item in attribute_category:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls, form):
        attribute_category = cls.query.filter_by(name=form.name.data, delete_time=None).first()
        if attribute_category is not None:
            return False

        item = cls.create(
            name=form.name.data,
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def edit(cls, id, form):
        attribute_category = cls.query.filter_by(id=id, delete_time=None).first()
        if attribute_category is None:
            return False

        item = attribute_category.update(
            id=id,
            name=form.name.data,
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def remove(cls, id):
        attribute_category = cls.query.filter_by(id=id, delete_time=None).first()
        if attribute_category is None:
            return False
        attribute_category.delete(commit=True)
        return True


class Brand(Brand):
    @classmethod
    def get_info(cls, item):
        info = {
            'id': item.id,
            'name': item.name,
            'list_pic_url': [] if item.list_pic_url.split('|') == [""] else item.list_pic_url.split(
                '|'),
            'simple_desc': item.simple_desc,
            'pic_url': [] if item.pic_url.split('|') == [""] else item.pic_url.split('|'),
            'sort_order': item.sort_order,
            'is_show': True if item.is_show == 1 else False,
            'floor_price': str(item.floor_price),
            'app_list_pic_url': [] if item.app_list_pic_url.split('|') == [
                ""] else item.app_list_pic_url.split('|'),
            'is_new': True if item.is_new == 1 else False,
            'new_pic_url': [] if item.new_pic_url.split('|') == [""] else item.new_pic_url.split(
                '|'),
            'new_sort_order': item.new_sort_order
        }
        return info

    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id=id, delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return info

    @classmethod
    def get_all(cls, params=None):
        brand = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            brand = brand.filter_by(delete_time=None).limit(size).offset(
                (int(page) - 1) * size).all()
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
    def search_by_name(cls, q, params=None):
        brand = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            brand = brand.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).limit(
                size).offset((int(page) - 1) * size).all()
        else:
            brand = brand.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).all()
        if not brand:
            return None
        items = []
        for item in brand:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls, form):
        brand = cls.query.filter_by(name=form.name.data, delete_time=None).first()
        if brand is not None:
            return False

        list_pic_url = cls.fiximgList(form.list_pic_url.data) if type(
            form.list_pic_url.data) == list else form.list_pic_url.data
        pic_url = cls.fiximgList(form.pic_url.data) if type(
            form.pic_url.data) == list else form.pic_url.data
        new_pic_url = cls.fiximgList(form.new_pic_url.data) if type(
            form.new_pic_url.data) == list else form.new_pic_url.data
        app_list_pic_url = cls.fiximgList(form.app_list_pic_url.data) if type(
            form.app_list_pic_url.data) == list else form.app_list_pic_url.data

        item = cls.create(
            name=form.name.data if form.name.data else '',
            list_pic_url=list_pic_url,
            simple_desc=form.simple_desc.data if form.simple_desc.data else '',
            pic_url=pic_url,
            sort_order=form.sort_order.data if form.sort_order.data else '50',
            is_show='1' if form.is_show.data is True else '0',
            floor_price=form.floor_price.data if form.floor_price.data else '0.00',
            app_list_pic_url=app_list_pic_url,
            is_new='1' if form.is_new.data is True else '0',
            new_pic_url=new_pic_url,
            new_sort_order=form.new_sort_order.data if form.new_sort_order.data else '100',
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def fiximgList(cls, imglist=[]):
        fix_list = []
        for item in imglist:
            temp = {
                "id": item['id'],
                "imgId": item['imgId'],
                "src": item['src'],
                "display": item['display'],
            }
            fix_list.append(temp)
        img_list_str = '|'.join('%s' % id for id in fix_list)
        return img_list_str

    @classmethod
    def edit(cls, id, form):
        brand = cls.query.filter_by(id=id, delete_time=None).first()
        if brand is None:
            return False

        list_pic_url = cls.fiximgList(form.list_pic_url.data) if type(
            form.list_pic_url.data) == list else form.list_pic_url.data
        pic_url = cls.fiximgList(form.pic_url.data) if type(
            form.pic_url.data) == list else form.pic_url.data
        new_pic_url = cls.fiximgList(form.new_pic_url.data) if type(
            form.new_pic_url.data) == list else form.new_pic_url.data
        app_list_pic_url = cls.fiximgList(form.app_list_pic_url.data) if type(
            form.app_list_pic_url.data) == list else form.app_list_pic_url.data

        item = brand.update(
            id=id,
            name=form.name.data if form.name.data else '',
            list_pic_url=list_pic_url,
            simple_desc=form.simple_desc.data if form.simple_desc.data else '',
            pic_url=pic_url,
            sort_order=form.sort_order.data if form.sort_order.data else '50',
            is_show='1' if form.is_show.data is True else '0',
            floor_price=form.floor_price.data if form.floor_price.data else '0.00',
            app_list_pic_url=app_list_pic_url,
            is_new='1' if form.is_new.data is True else '0',
            new_pic_url=new_pic_url,
            new_sort_order=form.new_sort_order.data if form.new_sort_order.data else '100',
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def remove(cls, id):
        brand = cls.query.filter_by(id=id, delete_time=None).first()
        if brand is None:
            return False
        item = brand.delete(commit=True)
        return True


class Category(Category):

    @classmethod
    def get_child(cls, id):
        category = cls.query
        category = category.filter_by(parent_id=id).filter_by(delete_time=None).order_by(
            cls.id.desc()).all()
        child = []
        if category:
            for item in category:
                info = {
                    "id": item.id,
                    "name": item.name,
                    "leaf": True if item.parent_id else False,
                    "children": cls.get_child(item.id)
                }
                child.append(info)
        return child

    @classmethod
    def fiximgList(cls, imglist=[]):
        fix_list = []
        for item in imglist:
            temp = {
                "id": item['id'],
                "imgId": item['imgId'],
                "src": item['src'],
                "display": item['display'],
            }
            fix_list.append(temp)
        img_list_str = '|'.join('%s' % id for id in fix_list)
        return img_list_str

    @classmethod
    def get_info(cls, item):
        children = cls.get_child(item.id)
        info = {
            'id': item.id,
            'name': item.name,
            "children": children,
            "leaf": False if children == [] else True
        }
        return info

    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id=id, delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return info

    @classmethod
    def get_all(cls, form):
        category = cls.query
        page = int(form.page.data) if form.page.data else 1
        size = int(form.size.data) if form.size.data else 20
        category = category.filter_by(parent_id='')
        if form.level.data:
            category = category.filter_by(level=form.level.data)
        if form.name.data:
            category = category.filter(cls.name.like('%' + form.name.data + '%'))
        category = category.filter_by(delete_time=None).order_by(cls.id.desc()).limit(size).offset(
            (int(page) - 1) * size).all()

        if not category:
            return None
        items = []
        for item in category:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def search_by_keywords(cls, form):
        category = cls.query
        page = int(form.page.data) if form.page.data else 1
        size = int(form.size.data) if form.size.data else 20
        if form.parent_id.data:
            category = category.filter_by(parent_id=form.parent_id.data)
        if form.level.data:
            category = category.filter_by(level=form.level.data)
        if form.name.data:
            category = category.filter(cls.name.like('%' + form.name.data + '%'))
        category = category.filter_by(delete_time=None).order_by(cls.id.desc()).limit(size).offset(
            (int(page) - 1) * size).all()
        if not category:
            return None
        items = []
        for item in category:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls, form):
        category = cls.query.filter_by(name=form.name.data, delete_time=None).first()
        if category is not None:
            return False

        front_name = form.front_name.data if form.front_name.data else ''
        front_desc = form.front_desc.data if form.front_desc.data else ''
        parent_id = form.parent_id.data if form.parent_id.data else '0'
        sort_order = form.sort_order.data if form.sort_order.data else '50'
        show_index = form.show_index.data if form.show_index.data else '0'
        banner_url = form.banner_url.data if form.banner_url.data else ''
        icon_url = form.icon_url.data if form.icon_url.data else ''
        img_url = cls.fiximgList(form.img_url.data) if type(
            form.img_url.data) == list else form.img_url.data
        wap_banner_url = form.wap_banner_url.data if form.wap_banner_url.data else ''
        level = form.level.data if form.level.data else ''
        Type = form.type.data if form.type.data else '0'

        item = cls.create(
            name=form.name.data,
            keywords=form.keywords.data,
            front_name=front_name,
            front_desc=front_desc,
            parent_id=parent_id,
            sort_order=sort_order,
            show_index=show_index,
            banner_url=banner_url,
            icon_url=icon_url,
            img_url=img_url,
            wap_banner_url=wap_banner_url,
            level=level,
            type=Type,
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def edit(cls, id, form):
        category = Category.query.filter_by(id=id, delete_time=None).first()
        if category is None:
            return False

        front_name = form.front_name.data if form.front_name.data else ''
        front_desc = form.front_desc.data if form.front_desc.data else ''
        parent_id = form.parent_id.data if form.parent_id.data else '0'
        sort_order = form.sort_order.data if form.sort_order.data else '50'
        show_index = form.show_index.data if form.show_index.data else '0'
        banner_url = form.banner_url.data if form.banner_url.data else ''
        icon_url = form.icon_url.data if form.icon_url.data else ''
        img_url = cls.fiximgList(form.img_url.data) if type(
            form.img_url.data) == list else form.img_url.data
        wap_banner_url = form.wap_banner_url.data if form.wap_banner_url.data else ''
        level = form.level.data if form.level.data else ''
        Type = form.type.data if form.type.data else '0'

        item = category.update(
            id=id,
            name=form.name.data,
            keywords=form.keywords.data,
            front_name=front_name,
            front_desc=front_desc,
            parent_id=parent_id,
            sort_order=sort_order,
            show_index=show_index,
            banner_url=banner_url,
            icon_url=icon_url,
            img_url=img_url,
            wap_banner_url=wap_banner_url,
            level=level,
            type=Type,
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def remove(cls, id):
        category = Category.query.filter_by(id=id, delete_time=None).first()
        if category is None:
            return False
        category.delete(commit=True)
        return True


class Keywords(Keywords):
    @classmethod
    def get_info(cls, item):
        info = {
            'id': item.id,
            'is_hot': item.is_hot,
            'is_default': item.is_default,
            'is_show': item.is_show,
            'scheme_url': item.scheme_url,
            'sort_order': item.sort_order,
            'type': item.type
        }
        return info

    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id=id, delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return info

    @classmethod
    def get_all(cls, params=None):
        keywords = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else 1
            size = params['size'] if 'size' in params else 20
            keywords = keywords.filter_by(delete_time=None).limit(size).offset(
                (int(page) - 1) * size).all()
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
    def new(cls, form):
        item = cls.create(
            is_hot=form.is_hot.data if form.is_hot.data else '0',
            is_default=form.is_default.data if form.is_default.data else '0',
            is_show=form.is_show.data if form.is_show.data else '1',
            scheme_url=form.scheme_url.data if form.scheme_url.data else '0',
            sort_order=form.sort_order.data if form.sort_order.data else '100',
            type=form.type.data if form.type.data else '0',
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def edit(cls, id, form):
        keywords = cls.query.filter_by(id=id, delete_time=None).first()
        if keywords is None:
            return False

        item = keywords.update(
            id=id,
            is_hot=form.is_hot.data if form.is_hot.data else '0',
            is_default=form.is_default.data if form.is_default.data else '0',
            is_show=form.is_show.data if form.is_show.data else '1',
            scheme_url=form.scheme_url.data if form.scheme_url.data else '0',
            sort_order=form.sort_order.data if form.sort_order.data else '100',
            type=form.type.data if form.type.data else '0',
            commit=True
        )
        info = cls.get_info(item)
        return info

    @classmethod
    def remove(cls, id):
        keywords = cls.query.filter_by(id=id, delete_time=None).first()
        if keywords is None:
            return False
        item = keywords.delete(commit=True)
        return True
