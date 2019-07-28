from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class Order(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_sn = Column(String(40),nullable=False,default='')
    member_id = Column(Integer, index=True,nullable=False,default='')
    order_status = Column(Integer,index=True,nullable=False,default='0')
    shipping_status = Column(Integer,index=True,nullable=False,default='0')
    pay_status = Column(Integer,index=True,nullable=False,default='0')
    consignee = Column(String(60),nullable=False,default='')
    country = Column(Integer,nullable=False,default='0')
    province = Column(Integer,nullable=False,default='0')
    city = Column(Integer,nullable=False,default='0')
    district = Column(Integer,nullable=False,default='0')
    address = Column(String(255),nullable=False,default='')
    mobile = Column(String(60),nullable=False,default='')
    postscript = Column(String(255),nullable=False,default='')
    shipping_fee = Column(DECIMAL(10,2),nullable=False,default='0.00')
    pay_name = Column(String(255),nullable=False,default='')
    pay_id = Column(Integer,index=True,nullable=False,default='0')
    actual_price = Column(DECIMAL(10,2),nullable=False,default='0.00')# 实际支付金额
    integral = Column(Integer,nullable=False,default='0')
    integral_money = Column(Integer,nullable=False,default='0.00')
    order_price = Column(DECIMAL(10,2),nullable=False,default='0.00')# 订单总价
    goods_price = Column(DECIMAL(10,2),nullable=False,default='0.00')# 商品总价
    add_time = Column(DateTime)
    confirm_time = Column(DateTime)
    pay_time = Column(DateTime)
    freight_price = Column(DECIMAL(10,2),nullable=False,default='0.00')# 配送费用
    coupon_id = Column(Integer,nullable=False,default='0')# 优惠卷id
    parent_id = Column(Integer,nullable=False,default='0')
    coupon_price = Column(DECIMAL(10,2),nullable=False,default='0.00')
    callback_status = Column(Boolean,nullable=False,default='True')
