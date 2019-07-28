from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class GoodsIssue(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    goods_id = Column(Integer,index=True,nullable=False,default='0')
    question = Column(Text)
    answer = Column(Text)