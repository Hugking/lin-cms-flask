from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class Feedback(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer,nullable=False,default='0')
    member_id = Column(Integer,index=True,nullable=False,default='0')
    title = Column(String(200),nullable=False,default='')
    type = Column(Integer,nullable=False,default='0')
    status = Column(Integer,nullable=False,default='0')
    content = Column(Text)
    time = Column(DateTime)
    img_url = Column(String(255),nullable=False,default='')
    order_id = Column(Integer,index=True,nullable=False,default='0')
    area = Column(Integer,nullable=False,default='0')