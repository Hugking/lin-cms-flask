from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer,Text,ForeignKey
from app.config.setting import PAGESIZE,current_page

class Attribute_category(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60),nullable=False,default='')

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
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
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
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
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

