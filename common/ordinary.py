"""通用函数插件"""
import random
import datetime
from flask import jsonify

PASSWORDLIBRARY = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
                   '8', '9']


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


def generate_password(length: int = 12) -> str:
    """生成随机密码
    :param length: 密码长度
    """
    max_number = len(PASSWORDLIBRARY) - 1
    return ''.join([PASSWORDLIBRARY[random.randint(0, max_number)] for _ in range(length)])


def generate_order_id():
    """生成订单编号"""
    randint = generate_verify_code()
    time = datetime.datetime.now().strftime("%M%f")
    return randint + time


def valid_random(core_random: str) -> bool:
    """验证core发送的随机码"""
    import plugins
    key = f'CoreRandom_{core_random}'
    result = plugins.Redis.get(key)
    plugins.Redis.delete(key)
    if result:
        return True
    else:
        return False
