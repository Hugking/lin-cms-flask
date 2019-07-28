from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class Collect(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer,index=True,nullable=False,default='0')
    value_id = Column(Integer,index=True,nullable=False,default='0')
    add_time = Column(DateTime)
    is_attention = Column(Integer,index=True,nullable=False,default='0')
    type_id = Column(Integer,nullable=False,default='0')
