from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, Text,ForeignKey

class Attribute(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    attribute_category_id = Column(Integer,index=True,nullable=False,default='0')
    name = Column(String(60),nullable=False,default='')
    input_type = Column(Integer,nullable=False,default='1')
    values = Column(Text,nullable=False)
    sort_order = Column(Integer,nullable=False,default='0')


