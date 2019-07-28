from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey

class Channel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False,default='')
    url = Column(String(255),nullable=False,default='')
    icon_url = Column(String(255),nullable=False,default='')
    sort_order = Column(Integer,nullable=False,default='10')