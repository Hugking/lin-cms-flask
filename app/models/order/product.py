from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class Product(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    goods_id = Column(Integer,ForeignKey('goods.id',onupdate='CASCADE'),nullable=False,default='0')
    goods_sn = Column(Integer,nullable=False,default='0')
    goods_number = Column(Integer,nullable=False,default='0')
    retail_price = Column(DECIMAL(10,2),nullable=False,default='0.00')
    goods_specifition_name_value = Column(Text)