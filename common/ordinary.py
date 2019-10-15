"""通用函数插件"""
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
