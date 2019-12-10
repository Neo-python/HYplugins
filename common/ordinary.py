"""通用函数插件"""
import random
import datetime
from flask import jsonify


def result_format(error_code: int = 0, data=None, message: str = '', **kwargs):
    if data is None:
        data = ''
    r = {
        'error_code': error_code,
        'data': data,
        'message': message,
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


def join_key(key: str, items: list) -> dict:
    """整理数据,通过字段值作为key"""
    result = dict()

    for item in items:
        result.update({getattr(item, key): item.serialization()})

    return result


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


def generate_order_id():
    """生成订单编号"""
    randint = generate_verify_code()
    time = datetime.datetime.now().strftime("%H%f")
    return randint + time
