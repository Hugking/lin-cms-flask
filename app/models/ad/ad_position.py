from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class AdPosition(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    width = Column(Integer,nullable=False,default='0')
    height = Column(Integer,nullable=False,default='0')
    name = Column(String(60),nullable=False,dafault='')
    desc = Column(String(255),nullable=False,dafault='')