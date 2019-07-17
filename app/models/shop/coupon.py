from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, Text,ForeignKey, DateTime,DECIMAL

class Coupon(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False,default='')
    type_money = Column(DECIMAL(10,2),nullable=False,default='0.00')
    send_type = Column(Integer,nullable=False,default='0')
    min_amount = Column(DECIMAL(10,2),nullable=False,default='0.00')
    max_amount = Column(DECIMAL(10,2),nullable=False,default='0.00')
    send_start_date = Column(DateTime)
    send_end_date = Column(DateTime)
    use_start_date = Column(DateTime)
    use_end_date = Column(DateTime)
    min_goods_amount = Column(DECIMAL(10,2),nullable=False,default='0.00')
