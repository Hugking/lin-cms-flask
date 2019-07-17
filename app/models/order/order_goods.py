from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class OrderGoods(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer,ForeignKey('order.id',onupdate='CASCADE'),nullable=False,default='0')
    goods_id = Column(Integer,ForeignKey('goods.id',onupdate='CASCADE'),nullable=False,default='0')
    goods_name = Column(String(255),nullable=False,default='')
    goods_sn = Column(Integer,nullable=False,default='0')
    product_id = Column(Integer,nullable=False,default='0')
    number = Column(Integer,nullable=False,default='0')
    market_price = Column(DECIMAL(10,2),nullable=False,default='0.00')
    retail_price = Column(DECIMAL(10,2),nullable=False,default='0.00')
    goods_specifition_name_value = Column(Text)
    list_pic_url = Column(String(255),nullable=False,default='')