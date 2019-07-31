wx_app = {
    'appid': 'wx37c9d625eddac654',
    'app_secret': '8d11a05dc9127dd9cfd23e28e03bba2b',
    'paykey': '02CBCE018C664DEB4462AB314B710193',
    'mch_id': '1531633161',
    'callback_url': 'http://test.wkaanig.cn/plugin/wx/callback',
    'refund_url': 'http://test.wkaanig.cn/plugin/wx/rcallback'
}
# 支付单

pay_status_display_mapping = {
    "0": "待支付",
    "1": "支付成功",
    "2": "退款成功",
    "-1": "部分退款",
    "-2": "支付取消"
}

pay_refund_status_display_mapping = {
    "0": "正在退款",
    "1": "退款成功",
    '-1': "退款失败"
}
