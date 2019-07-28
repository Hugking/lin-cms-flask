from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class TopicCategroy(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255),nullable=False,default='')
    pic_url = Column(String(255),nullable=False,default='')