import hashlib,requests,uuid,json,datetime
import xml.etree.ElementTree as ET
from flask import current_app as app
from app.config.secure import WX_APP
from app.models.third_client.pay_acccess_token import PayAccessToken
from app.libs.utils import get_current_date

import sys
import os

class WxPay():

    def __init__(self, merchant_key=None):
        self.merchant_key = merchant_key

    def create_sign(self, pay_data):
        """
        生成签名
        :return:
        """
        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.merchant_key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()

    def get_pay_info(self, pay_data=None):
        """
        获取支付信息
        :param xml_data:
        :return:
        """
        sign = self.create_sign(pay_data)
        pay_data['sign'] = sign
        xml_data = self.dict_to_xml(pay_data)
        headers = {'Content-Type': 'application/xml'}
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        r = requests.post(url=url, data=xml_data.encode('utf-8'), headers=headers)
        r.encoding = "utf-8"
        app.logger.info(r.text)
        if r.status_code == 200:
            prepay_id = self.xml_to_dict(r.text).get('prepay_id')
            pay_sign_data = {
                'appId': pay_data.get('appid'),
                'timeStamp': pay_data.get('out_trade_no'),
                'nonceStr': pay_data.get('nonce_str'),
                'package': 'prepay_id={0}'.format(prepay_id),
                'signType': 'MD5'
            }
            pay_sign = self.create_sign(pay_sign_data)
            pay_sign_data.pop('appId')
            pay_sign_data['paySign'] = pay_sign
            pay_sign_data['prepay_id'] = prepay_id
            return pay_sign_data

        return False
    
    def get_pay_reund_info(self, pay_data):
        """
        获取退款信息
        """
        sign = self.create_sign(pay_data)
        pay_data['sign'] = sign
        xml_data = self.dict_to_xml(pay_data)
        headers = {'Content-Type': 'application/xml'}
        url = "https://api.mch.weixin.qq.com/secapi/pay/refund"
        cert_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cert")
        weixinapiclient_cert = os.path.join(cert_path, "apiclient_cert.pem")
        weixinapiclient_key = os.path.join(cert_path, "apiclient_key.pem")
        r = requests.post(url=url, data=xml_data.encode('utf-8'), headers=headers,
        cert = (weixinapiclient_cert, weixinapiclient_key), verify = True)
        r.encoding = "utf-8"
        app.logger.info(r.text)
        if r.status_code == 200:
            res = self.xml_to_dict(r.text)
            if res.get('return_msg') == "OK":
                pay_sign_data = {
                    'out_trade_no': res.get('out_sign_no'),
                    'out_refund_no':res.get('out_refund_no'),
                    'refund_id': res.get('refund_id'),
                    'refund_fee':res.get('refund_fee'),
                    'total_fee': res.get('total_fee')
                }
                return pay_sign_data
            else:
                pay_sign_data = {
                    'err_code_desc':res.get('err_code') + res.get('err_code_desc'),
                    'out_trade_no': res.get('out_trade_no'),
                    'out_refund_no':res.get('out_refund_no'),
                    'refund_id': res.get('refund_id'),
                    'refund_fee':res.get('refund_fee'),
                    'total_fee': res.get('total_fee')
                }
                return pay_sign_data
        return False

    def dict_to_xml(self, dict_data):
        '''
        dict to xml
        :param dict_data:
        :return:
        '''
        xml = ["<xml>"]
        for k, v in dict_data.items():
            xml.append("<{0}>{1}</{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(self, xml_data):
        '''
        xml to dict
        :param xml_data:
        :return:
        '''
        xml_dict = {}
        root = ET.fromstring(xml_data)
        for child in root:
            xml_dict[child.tag] = child.text
        return xml_dict

    def get_nonce_str(self):
        '''
        获取随机字符串
        :return:
        '''
        return str(uuid.uuid4()).replace('-', '')

    def get_access_token(self):
        token = None
        token_info = PayAccessToken.query.filter(PayAccessToken.expired_time >= get_current_date()).first()
        if token_info:
            token = token_info.access_token
            return token

        config_mina = WX_APP
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}" \
            .format(config_mina['appid'], config_mina['app_secret'])

        r = requests.get(url=url)
        if r.status_code != 200 or not r.text:
            return token

        data = json.loads(r.text)
        now = datetime.datetime.now()
        date = now + datetime.timedelta(seconds=data['expires_in'] - 200)
        PayAccessToken.create(
            access_token = data['access_token'],
            expired_time = date.strftime("%Y-%m-%d %H:%M:%S"),
            commit = True
        )
        return data['access_token']
