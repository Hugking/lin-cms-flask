"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

# 安全性配置
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:password@localhost:3306/lin-cms'

SQLALCHEMY_ECHO = False

SECRET_KEY = '\x88W\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJJU\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*4'

WX_APP = {
    'appid': 'wx52590390436baa3f',
    'app_secret': '345b913e50def3df05665f794d7d6e5a',
    'paykey': 'xxxxxxxxxxxxxx换自己的',
    'mch_id': 'xxxxxxxxxxxx换自己的',
    'callback_url': '/api/order/callback'
}