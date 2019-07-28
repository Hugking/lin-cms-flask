from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class MemberLevel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False,default='')
    description = Column(String(255),nullable=False,default='')