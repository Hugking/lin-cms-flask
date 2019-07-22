"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from datetime import timedelta

# 分页配置
COUNT_DEFAULT = 10
PAGE_DEFAULT = 0
PAGESIZE = 10
current_page = 1

# 令牌配置
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# 屏蔽 sql alchemy 的 FSADeprecationWarning
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 插件模块暂时没有开启，以下配置可忽略
# plugin config写在字典里面
PLUGIN_PATH = {
    'poem': {'path': 'app.plugins.poem', 'enable': True, 'version': '0.0.1', 'limit': 20},
    'oss': {'path': 'app.plugins.oss', 'enable': True, 'version': '0.0.1', 'access_key_id': 'not complete', 'access_key_secret': 'not complete', 'endpoint': 'http://oss-cn-shenzhen.aliyuncs.com', 'bucket_name': 'not complete', 'upload_folder': 'app', 'allowed_extensions': ['jpg', 'gif', 'png', 'bmp']}
}

#支付单
PAY_STATUS_DISPLAY_MAPPING = {
    "0": "待支付",
    "1": "支付成功",
    "2": "退款成功",
    "-1": "部分退款",
    "-2": "支付取消"
}

PAY_REFUND_STATUS_DISPLAY_MAPPING = {
    "0": "正在退款",
    "1": "退款成功",
    '-1':"退款失败"
}