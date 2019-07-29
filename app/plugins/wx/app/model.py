from lin import db
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text


class Pay(Base):
    __tablename__ = 'pay'

    id = Column(Integer, primary_key=True)
    order_sn = Column(String(40), nullable=False, unique=True)
    member_id = Column(Integer, nullable=False)
    pay_price = Column(Numeric(10, 2), nullable=False)
    pay_sn = Column(String(128), nullable=False)
    prepay_id = Column(String(128), nullable=False)
    note = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)
    pay_time = Column(DateTime)


class PayAccessToken(Base):
    __tablename__ = 'pay_access_token'

    id = Column(Integer, primary_key=True)
    access_token = Column(String(600), nullable=False)
    expired_time = Column(DateTime)


class PayCallbackData(Base):
    __tablename__ = 'pay_callback_data'

    id = Column(Integer, primary_key=True)
    pay_id = Column(Integer, nullable=False, unique=True)
    pay_data = Column(Text, nullable=False)
    refund_data = Column(Text, nullable=False)


class PayRefund(Base):
    __tablename__ = 'pay_refund'

    id = Column(Integer, primary_key=True)
    pay_id = Column(Integer, nullable=False)
    refund_sn = Column(String(128), nullable=False)
    refund_fee = Column(Numeric(10, 2), nullable=False)
    refund_desc = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)


class ThirdBind(Base):
    __tablename__ = 'third_bind'

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False)
    client_type = Column(String(20), nullable=False)
    openid = Column(String(80), nullable=False)
    union_id = Column(String(100), nullable=False)


class QueueList(Base):
    __tablename__ = 'queue_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    queue_name = Column(String(30), nullable=False, default=' ')
    data = Column(String(500), nullable=False, default='')
    status = Column(Integer, nullable=False, default='-1')


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(100), nullable=False, default=' ')
    mobile = Column(String(11), nullable=False, default=' ')
    sex = Column(Integer, nullable=False, default='0')
    avatar = Column(String(200), nullable=False, default=' ')
    salt = Column(String(32), nullable=False, default=' ')
    reg_ip = Column(String(100), nullable=False, default=' ')
    username = Column(String(255), nullable=False, default='')
    password = Column(String(255), nullable=False, default='')
    level_id = Column(Integer, index=True, nullable=False, default='1')
    status = Column(Integer, nullable=False, default='1')
