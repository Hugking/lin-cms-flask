from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class GoodsSpecification(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    goods_id = Column(Integer,ForeignKey('goods.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False,default='0')
    specification_id = Column(Integer,Index=True,nullable=False,default='0')
    value = Column(String(255),nullable=False,default='')
    pic_url = Column(String(255),nullable=False,default='')