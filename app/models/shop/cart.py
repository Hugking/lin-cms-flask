from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text,Index, ForeignKey

class Cart(Base):
    id = Column(Integer, primary_key=True, autoincrement=True) 
    member_id = Column(Integer,index=True,nullable=False, default='0')
    session_id = Column(String(32),index=True,nullable=False, default='')
    goods_id = Column(Integer,nullable=False, default='0')
    goods_sn = Column(String(60),nullable=False, default='')
    product_id = Column(Integer,nullable=False, default='0')
    goods_name = Column(String(120),nullable=False, default='')
    market_price = Column(DECIMAL(10,2),nullable=False, default='0.00')
    retail_price = Column(DECIMAL(10,2) ,nullable=False, default='0.00')
    number = Column(Integer,nullable=False, default='0')
    goods_specifition_name_value = Column(Text ,nullable=False)#'规格属性组成的字符串，用来显示用'
    goods_specifition_ids = Column(String(60) ,nullable=False, default='')#'product表对应的goods_specifition_ids'
    checked = Column(Integer,nullable=False,default='1')
    list_pic_url = Column(String(255) ,nullable=False, default='')