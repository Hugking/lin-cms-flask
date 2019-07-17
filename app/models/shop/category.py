from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,Index

class Category(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(90),nullable=False,default='')
    keywords = Column(String(255),nullable=False,default='')
    front_desc = Column(String(255),nullable=False,default='')
    parent_id = Column(Integer,index=True,nullable=False,default='0')
    sort_order = Column(Integer,nullable=False,default='50')
    show_index = Column(Integer,nullable=False,default='0')
    is_show = Column(Integer,nullable=False,default='1')
    banner_url = Column(String(255),nullable=False,default='')
    icon_url = Column(String(255),nullable=False,default='')
    img_url = Column(String(255),nullable=False,default='')
    wap_banner_url = Column(String(255),nullable=True,default='')
    level = Column(String(255),nullable=False,default='')
    type = Column(Integer,nullable=False,default='0')
    front_name = Column(String(255),nullable=False,default='')
