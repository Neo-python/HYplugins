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
