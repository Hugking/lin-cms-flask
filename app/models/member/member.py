from lin.exception import NotFound, ParameterException,Success
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer,ForeignKey

class Member(Base): 
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(100),nullable=False, default=' ')
    mobile = Column(String(11), nullable=False, default=' ')
    sex = Column(Integer, nullable=False, default='0')
    avatar = Column(String(200), nullable=False, default=' ')
    salt = Column(String(32), nullable=False, default=' ')
    reg_ip = Column(String(100), nullable=False, default=' ')
    username = Column(String(255),nullable=False,default='')
    password = Column(String(255),nullable=False,default='')
    level_id = Column(Integer,ForeignKey('member_level.id',onupdate='CASCADE'),nullable=False,default='1')
    status = Column(Integer, nullable=False,default='1')

    # @classmethod
    # def get_member_info(cls, form):
    #     member_info = cls.query.filter_by(id=form.member_id.data, delete_time=None).first()
    #     if member_info is not None:
    #         return member_info
    #     return None
    
    # @classmethod
    # def member_share(cls, form):
    #     member_info = cls.query.filter_by(member_id=form.member_id.data, delete_time=None).first()
