from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class Region(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer,index=True,nullable=False,default='0')
    name = Column(String(255),nullable=False,default='')
    type = Column(Integer,index=True,nullable=False,default='2')
    agency_id = Column(Integer,index=True,nullable=False,default='0')