from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index
from app.config.setting import PAGESIZE,current_page

class Keywords(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_hot = Column(Integer,index=True,nullable=False,default='0')
    is_default = Column(Integer,index=True,nullable=False,default='0')
    is_show = Column(Integer,index=True,nullable=False,default='1')
    sort_order = Column(Integer,index=True,nullable=False,default='100')
    scheme_url = Column(String(255),index=True,nullable=False,default='')# 跳转连接
    type = Column(Integer,index=True,nullable=False,default='0')

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
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
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
