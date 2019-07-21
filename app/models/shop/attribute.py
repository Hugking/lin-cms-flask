from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, Text,ForeignKey
from app.config.setting import PAGESIZE,current_page
from app.models.shop.attribute_category import Attribute_category

class Attribute(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    attribute_category_id = Column(Integer,index=True,nullable=False,default='0')
    name = Column(String(60),nullable=False,default='')
    input_type = Column(Integer,nullable=False,default='1')
    values = Column(Text,nullable=False)
    sort_order = Column(Integer,nullable=False,default='0')

    @classmethod
    def get_info(cls,item):
        info = {
            'id' :item.id,
            'attr_cate':item.get_attr_cate,
            'name':item.name,
            'input_type':item.input_type,
            'values':item.values,
            'sort_order':item.sort_order
        }
        return info

    @property
    def get_attr_cate(cls):
        attribute_category = Attribute_category.query.filter_by(id = cls.attribute_category_id,delete_time=None).first()
        if attribute_category is None:
            return '无匹配'
        return  attribute_category.name


    @classmethod
    def get_detail(cls, id):
        item = cls.query.filter_by(id = id,delete_time=None).first()
        if not item:
            return None
        info = cls.get_info(item)
        return  info
        
    @classmethod
    def get_all(cls,params=None):
        attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
            attribute = attribute.filter_by(delete_time=None).limit(size).offset((int(page) - 1) * size).all()
        else:
            attribute = attribute.filter_by(delete_time=None).all()
        if not attribute:
            return None
        items = []
        for item in attribute:
            info = cls.get_info(item)
            items.append(info)
        return items
    
    @classmethod
    def search_by_name(cls,q,params=None):
        attribute = cls.query
        if params is not None:
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
            attribute = attribute.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).limit(size).offset((int(page) - 1) * size).all()
        else:
            attribute =  attribute.filter(cls.name.like('%' + q + '%'), cls.delete_time == None).all()
        if not attribute:
            return None
        items = []
        for item in attribute:
            info = cls.get_info(item)
            items.append(info)
        return items

    @classmethod
    def new(cls,form):
        attribute = cls.query.filter_by(name = form.name.data,delete_time=None).first()
        if attribute is not None :
            return False

        attribute_category = Attribute_category.query.filter_by(id = int(form.attribute_category_id.data),delete_time=None).first()
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
        
        attribute_category = Attribute_category.query.filter_by(id = int(form.attribute_category_id.data),delete_time=None).first()
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
