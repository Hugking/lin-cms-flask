from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class Keywords(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_hot = Column(Integer,Index=True,nullable=False,default='0')
    is_default = Column(Integer,Index=True,nullable=False,default='0')
    is_show = Column(Integer,Index=True,nullable=False,default='1')
    sort_order = Column(Integer,Index=True,nullable=False,default='100')
    scheme_url = Column(String(255),Index=True,nullable=False,default='')# 跳转连接
    type = Column(Integer,Index=True,nullable=False,default='0')