from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class RelatedGoods(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    goods_id = Column(Integer,Index=True,nullable=False,default='0')
    related_goods_id = Column(Integer,Index=True,nullable=False,default='0')