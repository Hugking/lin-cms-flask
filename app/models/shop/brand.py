from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL,Index
from app.config.setting import PAGESIZE,current_page
class Brand(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False,default='')
    list_pic_url = Column(String(255),nullable=False,default='')
    simple_desc = Column(String(255),nullable=False,default='')
    pic_url = Column(String(255),nullable=False,default='')
    sort_order = Column(Integer,nullable=False,default='50')
    is_show = Column(Integer,index=True,nullable=False,default='1')
    floor_price = Column(DECIMAL(10,2),nullable=False,default='0.00')
    app_list_pic_url = Column(String(255),nullable=False,default='')
    is_new = Column(Integer,nullable=False,default='0')
    new_pic_url = Column(String(255),nullable=False,default='')
    new_sort_order = Column(Integer,nullable=False,default='100')

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
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
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
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
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
