from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, Text

class PayCallbackData(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pay_id = Column(Integer, nullable=False, unique=True, default='0')
    pay_data = Column(Text, nullable=False,default='')
    refund_data = Column(Text, nullable=False,default='')