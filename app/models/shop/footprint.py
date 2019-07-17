from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, Text,ForeignKey, DateTime

class Footprint(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer,ForeignKey('member.id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False,default='0')
    goods_id = Column(Integer,ForeignKey('goods.id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False,default='0')
    add_time = Column(DateTime)
