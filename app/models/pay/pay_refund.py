from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, Text, String, Numeric
from app.config.setting import PAY_REFUND_STATUS_DISPLAY_MAPPING

class PayRefund(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pay_id = Column(Integer, nullable=False, default='0')
    refund_sn = Column(String(128), nullable=False, default='')
    refund_fee =  Column(Numeric(10, 2), nullable=False, default='0.00')
    refund_desc = Column(Text, nullable=False,default='')
    status = Column(Integer, nullable=False, default='0')

    @property
    def status_desc(self):
        return PAY_REFUND_STATUS_DISPLAY_MAPPING[str(self.status)]