from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index, Boolean

class Topic(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255),nullable=False,default='')
    content = Column(Text)
    avatar = Column(String(255),nullable=False,default='')
    item_pic_url = Column(String(255),nullable=False,default='')
    subtitle = Column(String(255),nullable=False,default='')
    topic_categroy_id = Column(Integer,nullable=False,default='0')
    price_info = Column(DECIMAL(10,2),nullable=False,default='')
    read_count = Column(Integer,nullable=False,default='0')
    scene_pic_url = Column(String(255),nullable=False,default='')
    topic_template_id = Column(Integer,nullable=False,default='0')
    topic_tag_id = Column(Integer,nullable=False,default='0')
    is_show = Column(Integer,nullable=False,default='0')
    sort_order = Column(Integer,nullable=False,default='0')