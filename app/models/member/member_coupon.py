from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class MemberCoupon(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer,index=True,nullable=False,default='0')
    coupon_id = Column(Integer,nullable=False,default='0')
    coupon_number = Column(Integer,nullable=False,default='0') 
    used_time = Column(DateTime,nullable=False,default='')
    order_id = Column(Integer,nullable=False,default='0')