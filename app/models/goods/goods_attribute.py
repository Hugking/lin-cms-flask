from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class GoodsAttribute(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    goods_id = Column(Integer,index=True,nullable=False,default='0')
    attribute_id = Column(Integer,index=True,nullable=False,default='0')
    value = Column(Text)
