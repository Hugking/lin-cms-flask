from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, DECIMAL,Text, ForeignKey,DateTime,Index

class Comment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer,nullable=False,default='0')
    value_id = Column(Integer,index=True,nullable=False,default='0')
    content = Column(Text,nullable=False,default='')
    add_time = Column(DateTime)
    status = Column(Integer,nullable=False,default='0')
    member_id = Column(Integer,index=True,nullable=False,default='0')
    new_comment = Column(Text,nullable=False,default='')
    
