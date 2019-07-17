from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class SearchHistory(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(255),nullable=False,default='')
    From = Column(String(255),nullable=False,default='')
    member_id = Column(Integer,index=True,nullable=False,default='0')
