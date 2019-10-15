from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


class SMS:
    """腾讯短信接口"""

    def __init__(self, app_id: str, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.init()

    def init(self):
        """初始化对象"""
        self.sms = SmsSingleSender(self.app_id, self.app_key)

    def send(self, template_id, phone_number: str, params, sms_sign: str = '', nation_code=86):
        try:
            # 签名参数未提供或者为空时，会使用默认签名发送短信
            result = self.sms.send_with_param(nation_code, phone_number, template_id, params=params, sign=sms_sign,
                                              extend="", ext="")
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            print(result)
