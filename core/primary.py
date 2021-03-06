"""中台相关"""
import config
import requests
import json
from flask import jsonify
from plugins.HYplugins.error import ViewException


class CoreApi:
    """核心中台接口"""
    interface = f'http://127.0.0.1:{config.core_server_port}'

    @staticmethod
    def understand(api_result) -> dict:
        """处理接口响应"""
        return jsonify(json.loads(api_result.content.decode()))

    def send_sms(self, **kwargs):
        """通知中台发送短信,接收一个参数,此参数一般情况下为短信验证码.
        :param kwargs:
        :param kwargs: phone: str
        :param kwargs: code: str
        :param kwargs: template_id: str
        """
        interface_path = '/send_sms/code/'
        url = f'{self.interface}{interface_path}'
        result = requests.post(url, json=kwargs)
        return self.understand(api_result=result)

    def notice_sms(self, **kwargs):
        """通知中台发送管理员通知短信,群体发送.
        :param kwargs:
        :param kwargs: params: list
        :param kwargs: template_id: str
        """
        interface_path = '/send_sms/notice_manager/'
        url = f'{self.interface}{interface_path}'
        result = requests.post(url, json=kwargs)
        return self.understand(api_result=result)

    def upload_url(self, **kwargs) -> dict:
        """通知中通获取图片上传授权地址
        :param kwargs:
        :param kwargs: user_uuid:str
        :param kwargs: genre:str
        :param kwargs: suffix:str
        :return:
        """
        interface_path = '/upload_url/'
        url = f'{self.interface}{interface_path}'
        result = requests.get(url, params=kwargs)
        return self.understand(api_result=result)

    def upload_credentials(self, **kwargs):
        """通知中通获取图片上传授权地址
        :param kwargs:
        :param kwargs: user_uuid:str
        :param kwargs: genre:str
        :param kwargs: suffix:str
        :return:
                """
        interface_path = '/upload_credentials/'
        url = f'{self.interface}{interface_path}'
        result = requests.get(url, params=kwargs)
        return self.understand(api_result=result)

    def get_open_id(self, **kwargs) -> dict:
        """获取open_id
        :param kwargs: code:微信code
        :param kwargs: port:当前应用端口号
        :return:
        """
        interface_path = '/get_open_id/'
        url = f'{self.interface}{interface_path}'
        result = requests.get(url, params=kwargs)
        result = result.json()
        if result.get('error_code') != 0:
            raise ViewException(error_code=5000, message="应用未能正常调用微信接口,请联系管理员处理.")
        return result['data']

    def batch_sms(self, **kwargs):
        """批量发送短信,此接口为异步接口.
        :param kwargs:
        :param kwargs: template_id:str 短信模板编号
        :param kwargs: phone_list:list 短信接收者手机号
        :param kwargs: params:list     短信模板对应参数
        :return:
        """
        interface_path = '/send_sms/batch/'
        url = f'{self.interface}{interface_path}'
        result = requests.post(url, json=kwargs)
        return self.understand(api_result=result)

    def position_distance(self, **kwargs):
        """计算位置距离
        origin原点只支持单点
        destinations目标点支持多点
        :return:
        """

        interface_path = '/position/distance/'
        url = f'{self.interface}{interface_path}'
        result = requests.post(url, json=kwargs)
        return self.understand(api_result=result)

    def clear_token(self, **kwargs):
        """清除用户token,强制更新其token
        :param kwargs: port: 应用端口号,用来分辨具体应用
        :param kwargs: uuid: 用户编号
        :return:
        """

        interface_path = '/token/clear/'
        url = f'{self.interface}{interface_path}'
        result = requests.get(url, params=kwargs)
        return self.understand(api_result=result)
