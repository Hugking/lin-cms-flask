from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, Text,ForeignKey

class Attribute(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    attribute_category_id = Column(Integer,ForeignKey('attribute_category.id', ondelete='CASCADE', onupdate='CASCADE'))
    name = Column(String(60),nullable=False,default='')
    input_type = Column(Integer,nullable=False,default='1')
    values = Column(Text,nullable=False)
    sort_order = Column(Integer,nullable=False,default='0')


