"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from app.config.setting import BaseConfig

class DevelopmentSecure(BaseConfig):
    """
    开发环境安全性配置
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:password@localhost:3306/lin-cms'

    SQLALCHEMY_ECHO = False

    SECRET_KEY = '\x88W\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJJU\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*4'


class ProductionSecure(BaseConfig):
    """
    生产环境安全性配置
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:password@localhost:3306/lin-cms'

    SQLALCHEMY_ECHO = False

    SECRET_KEY = '\x88W\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJJU\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*4'

WX_APP = {
    'appid': 'wx37c9d625eddac654',
    'app_secret': '8d11a05dc9127dd9cfd23e28e03bba2b',
    'paykey': '02CBCE018C664DEB4462AB314B710193',
    'mch_id': '1531633161',
    'callback_url': '/wx/pay/callback',
    'refund_url':'/wx/pay/rcallback'
}

APP = {
    'domain': 'http://flask.wkaanig.cn'
}

