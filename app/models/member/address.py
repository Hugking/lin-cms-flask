from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class Address(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False,default='')
    member_id = Column(Integer,ForeignKey('member.id',onupdate="CASCADE"),nullable=False,dafault='0')
    country_id = Column(Integer,nullable=False,dafault='0')
    province_id = Column(Integer,nullable=False,dafault='0')
    city_id = Column(Integer,nullable=False,dafault='0')
    district_id = Column(Integer,nullable=False,dafault='0')
    address = Column(String(255),nullable=False,default='')
    mobile = Column(String(255),nullable=False,default='')
    is_default = Column(Integer,nullable=False,dafault='0')