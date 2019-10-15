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


def orm_func(func_name: str, *args, **kwargs):
    """orm序列化,funcs参数便捷生成函数"""
    if not len(args):
        args = tuple()
    if not len(kwargs):
        kwargs = dict()
    return func_name, args, kwargs


def paginate_info(paginate, items):
    """分页信息"""
    result = {
        'total': paginate.total,
        'page': paginate.page,
        'max_page': paginate.pages,
        'items': items
    }
    return result


class NeoDict(dict):

    def __getattr__(self, item):
        """快捷获取字典表数据"""
        return self[item]


def generate_verify_code(length: int = 4) -> str:
    """生成数字验证码
    :param length: 验证码长度
    """

    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
