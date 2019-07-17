from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class CommentPicture(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(Integer,ForeignKey('comment.id',ondelete='CASCADE', onupdate='CASCADE'),nullable=False,default='0')
    pic_url = Column(String(255),nullable=False,default='')
    sort_order = Column(Integer,nullable=False,default='5')
