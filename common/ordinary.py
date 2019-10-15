"""通用函数插件"""
import random
from flask import jsonify


def result_format(error_code: int = 0, data=None, **kwargs):
    if data is None:
        data = ''
    r = {
        'error_code': error_code,
        'data': data,
        **kwargs
    }
    return jsonify(r)


class NeoDict(dict):

    def __getattr__(self, item):
        """快捷获取字典表数据"""
        return self[item]


def generate_verify_code(length: int = 4) -> str:
    """生成数字验证码
    :param length: 验证码长度
    """

    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
