from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class OrderExpress(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer,index=True,nullable=False,default='0')
    shipper_id = Column(Integer,nullable=False,default='0')
    shipper_name = Column(String(255),nullable=False,default='')# 物流公司名称
    shipper_code = Column(String(255),nullable=False,default='')# 物流公司代码
    logistic_code = Column(String(255),nullable=False,default='')# 快递单号
    traces = Column(String(2000),nullable=False,default='')# 物流跟踪信息
    is_finish = Column(Integer,nullable=False,default='0')
    request_count = Column(Integer,nullable=False,default='0')# 总查询次数
    request_time = Column(DateTime)# 最近向第三方物流查询时间
    
