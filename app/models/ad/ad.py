from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class Ad(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_position_id = Column(Integer,index=True,nullable=False,dafault='0')
    media_type = Column(Integer,nullable=False,dafault='0')
    name = Column(String(60),nullable=False,dafault='')
    link = Column(String(255),nullable=False,dafault='')
    img_url = Column(String(255),nullable=False,dafault='')
    content = Column(String(255),nullable=False,dafault='')
    end_time = Column(DateTime,nullable=False,dafault='')
    is_show = Column(Integer,index=True,nullable=False,dafault='1')