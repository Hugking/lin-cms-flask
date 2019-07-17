from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class Shipper(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20),nullable=False,default='')
    code = Column(String(10),nullable=False,default='')
    sort_order = Column(Integer,nullable=False,default='10')
