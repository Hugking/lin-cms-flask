from lin.interface import InfoCrud as Base
from sqlalchemy import Column, DateTime, Integer, String

class PayAccessToken(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    access_token = Column(String(600), nullable=False,default='')
    expired_time = Column(DateTime)