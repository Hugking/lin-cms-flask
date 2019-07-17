from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL,Index

class Brand(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False,default='')
    list_pic_url = Column(String(255),nullable=False,default='')
    simple_desc = Column(String(255),nullable=False,default='')
    pic_url = Column(String(255),nullable=False,default='')
    sort_order = Column(Integer,nullable=False,default='')
    is_show = Column(Integer,index=True,nullable=False,default='1')
    floor_price = Column(DECIMAL(10,2),nullable=False,default='0.00')
    app_list_pic_url = Column(String(255),nullable=False,default='')
    is_new = Column(Integer,nullable=False,default='0')
    new_pic_url = Column(String(255),nullable=False,default='')
    new_sort_order = Column(Integer,nullable=False,default='100')
