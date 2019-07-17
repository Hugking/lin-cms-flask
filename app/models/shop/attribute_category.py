from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer,Text,ForeignKey

class Attribute_category(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60),nullable=False,default='')
    enable = Column(Integer,nullable=False,default='1')

