from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class GoodsGallery(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    goods_id = Column(Integer,ForeignKey('goods.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False,default='0')
    img_url = Column(String(255),nullable=False,default='')
    img_desc = Column(String(255),nullable=False,default='')
    sort_order = Column(Integer,nullable=False,default='5')
