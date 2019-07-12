from lin.exception import NotFound, ParameterException,Success
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer

from flask import app,json
from app.config.secure import WX_APP
from app.models.member.member import Member
import hashlib, requests, random, string


class ThirdBind(Base): 
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, nullable=False, default='0')
    client_type = Column(String(20), nullable=False, default='')
    openid = Column(String(80), nullable=False, default='')
    union_id = Column(String(100), nullable=False, default='')

    @classmethod
    def get_wechat_openid(cls,form):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(WX_APP['appid'], WX_APP['app_secret'], form.code.data)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        else:
            return -1
        return openid

    @classmethod
    def wx_check_openid(cls, form):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        openid = cls.get_wechat_openid(form)
        if openid is None:
            resp['code'] = -1
            resp['msg'] = "调用微信出错"
            return resp
        if openid is -1:
            resp['code'] = -2
            resp['msg'] = "code已使用"
            return resp
        return openid

    @classmethod
    def wx_check_reg(cls, form):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        openid = cls.wx_check_openid(form)
        bind_info = cls.query.filter_by(openid=openid, delete_time=None).first()
        if bind_info is None:
            resp['code'] = -1
            resp['msg'] = "未绑定"
            return resp
        member_info = Member.query.filter_by(id=bind_info.member_id, delete_time=None).first()
        if member_info is None:
            resp['code'] = -1
            resp['msg'] = "未查询到绑定信息"
            return resp
        token = "%s#%s" % (cls.generate_auth_code(member_info), member_info.id)
        resp['data'] = {'token': token}
        resp['data']['info'] = {
        "member_id":member_info.id,
        "nickname": member_info.nickname,
        "avatar_url": member_info.avatar
        }
        return resp
    
    @classmethod
    def wx_register(cls, form):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        openid = cls.wx_check_openid(form)
        bind_info = cls.query.filter_by(openid=openid, delete_time=None).first()
        if bind_info is not None:
            member_info = Member.query.filter_by(id=bind_info.member_id, delete_time=None).first()
            if member_info is None:
                resp['code'] = -1
                resp['msg'] = "未查询到绑定信息"
                return resp
        member_info = Member.create(
            nickname = form.userInfo.data['nickName'],
            sex=form.userInfo.data['gender'],
            avatar = form.userInfo.data['avatarUrl'],
            salt = cls.generate_salt(),
            commit=True
        )
        cls.create(
            member_id = member_info.id,
            client_type = 'wx',
            openid = openid,
            commit=True
        )
        token = "%s#%s" % (cls.generate_auth_code(member_info), member_info.id)
        resp['data'] = {'token': token}
        return resp

    @staticmethod
    def generate_auth_code(member_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def generate_salt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(keylist)
