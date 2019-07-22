from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,Index


from app.models.shop.keywords import Keywords
from app.config.setting import PAGESIZE,current_page

class Category(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(90),nullable=False,default='')
    keywords = Column(String(255),nullable=False,default='')
    front_desc = Column(String(255),nullable=False,default='')
    parent_id = Column(Integer,index=True,nullable=False,default='0')
    sort_order = Column(Integer,nullable=False,default='50')
    show_index = Column(Integer,nullable=False,default='0')
    banner_url = Column(String(255),nullable=False,default='')
    icon_url = Column(String(255),nullable=False,default='')
    img_url = Column(String(255),nullable=False,default='')
    wap_banner_url = Column(String(255),nullable=False,default='')
    level = Column(String(255),nullable=False,default='')
    type = Column(Integer,nullable=False,default='0')
    front_name = Column(String(255),nullable=False,default='')

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
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
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
            page = params['page'] if 'page' in params else current_page
            size = params['size'] if 'size' in params else PAGESIZE
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


        

            