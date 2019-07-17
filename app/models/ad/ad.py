from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class Ad(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_position_id = Column(Integer,index=True,nullable=False,default='0')
    media_type = Column(Integer,nullable=False,default='0')
    name = Column(String(60),nullable=False,default='')
    link = Column(String(255),nullable=False,default='')
    img_url = Column(String(255),nullable=False,default='')
    content = Column(String(255),nullable=False,default='')
    end_time = Column(DateTime,nullable=False,default='')
    is_show = Column(Integer,index=True,nullable=False,default='1')