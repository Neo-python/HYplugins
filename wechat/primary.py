"""微信相关接口"""
import requests
from flask import request


class WechatApi:
    """微信接口"""

    def __init__(self, app_id: str, app_secret: str):
        """对象初始化"""
        self.app_id = app_id
        self.app_secret = app_secret

    def get_open_id(self):
        """获取open_id"""
        if request.get_json(force=True).get('code'):
            return request.get_json(force=True).get('code')
        real_code = request.get_json(force=True).get('real_code')
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={self.app_id}&secret={self.app_secret}&js_code={real_code}&grant_type=authorization_code'
        result = requests.get(url)
        result = result.json()
        return result['openid']
