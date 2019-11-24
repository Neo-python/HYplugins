"""中台相关"""
import config
import requests
import json
from flask import jsonify


class CoreApi:
    """核心中台接口"""
    interface = f'http://127.0.0.1:{config.core_server_port}'

    @staticmethod
    def understand(api_result) -> dict:
        """处理接口响应"""
        return jsonify(json.loads(api_result.content.decode()))

    def send_sms(self, **kwargs):
        """通知中台发送短信
        :param kwargs:
        :param kwargs: phone: str
        :param kwargs: code: str
        :param kwargs: template_id: str
        """
        interface_path = '/send_sms/code/'
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

    def get_open_id(self, **kwargs):
        """获取open_id
        :param kwargs: code:微信code
        :param kwargs: port:当前应用端口号
        :return:
        """
        interface_path = '/get_open_id/'
        url = f'{self.interface}{interface_path}'
        result = requests.get(url, params=kwargs)
        return self.understand(api_result=result)

    def batch_sms(self, **kwargs):
        """批量发送短信
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
