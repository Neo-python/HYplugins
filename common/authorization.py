import time
import json
from functools import wraps
from flask import request, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadSignature
import plugins
from plugins.common.authorization import LoginVerify
from plugins.HYplugins.error import ViewException
from plugins.HYplugins.common import NeoDict

auth = HTTPTokenAuth()


def authorization_to_dict(authorization: str) -> dict:
    """HTTP头Authorization转换数据类型为dict"""
    items = authorization.split(',')  # 以','拆分出键值对
    items = (i.split('=') for i in items)  # 以'='拆分键值对
    try:
        result = dict(items)  # 转换为字典表
    except BaseException as err:
        print(err)
        result = dict()  # 转换失败 设置空字典表返回
    return result


@auth.verify_token
def _verify_token(authorization):
    """验证token,@auth.login_required 所调用的验证逻辑
    :param authorization:HTTP.Headers.Authorization -> Bearer
    """
    authorization = authorization_to_dict(authorization)  # 解析Authorization数据,返回dict类型数据集合

    token = authorization.get('token', None)  # 获取token值
    try:
        assert token, 'authorization failed'
        payload = plugins.serializer.loads(token)  # 尝试解密token
        sub = payload.get('uuid')  # 获取用户uuid
        redis_cache = plugins.Redis.get(f'UserInfo_{sub}')

        # 检查记录是否存在
        if not redis_cache:
            raise ViewException(error_code=4003, message='token信息错误')
        # 存在记录,进行数据转换
        redis_cache = NeoDict(**json.loads(redis_cache))
        if redis_cache.get('iat') != payload.get('iat'):
            raise ViewException(error_code=4002, message='token过期')
    except AssertionError as err:
        raise ViewException(error_code=4001, message="错误的token", system_message=str(err))

    except BadSignature:
        raise ViewException(error_code=4003, message='token信息错误')
    else:
        g.user = redis_cache  # 刷新token时调用
        return True


def login(**login_kwargs):
    """登录权限验证装饰器.
    login调用示例: @login(demo={'args':0})
    login_kwargs = {func_name:{args_name:args}}
    """

    def outer(func):
        @auth.login_required
        @wraps(func)
        def inner(*args, **kwargs):
            """自定义验证逻辑,此阶段为"已验证过token信息有效性为有效"之后"""
            verify = LoginVerify()
            for func_name, func_kwargs in login_kwargs.items():
                verify_func = getattr(verify, func_name)
                verify_func(**func_kwargs)
            return func(*args, **kwargs)

        return inner

    return outer


def check_sign_in():
    """检查登录状态"""

    authorization = request.headers.get('Authorization')
    if authorization:
        authorization = authorization.replace('Bearer ', '')

    if authorization:
        try:
            _verify_token(authorization=authorization)
        except Exception:
            return None
        else:
            return True
    else:
        return None


def get_user_info(error_out: bool = True):
    """获取用户数据:缓存数据"""

    def _get_user_info():
        _info = getattr(g, '_info', None)
        if _info:
            return _info
        user_info = getattr(g, 'user', None)
        if user_info and user_info.get('sub', None):
            user_uuid = user_info.get('sub')
            g._info = """Redis.get(f'{config.USER_REDIS_KEY_PREFIX}_info_{user_uuid}')"""
            return g._info
        else:
            return None

    result = _get_user_info()
    if result:
        try:
            result = NeoDict(**json.loads(result))
        except:
            raise ViewException(error_code=4004, message='用户数据异常!!!')
        else:
            return result
    elif error_out is True:
        raise ViewException(error_code=4004, message='用户数据异常!!!')


class Token:

    def __init__(self, user):
        self.user = user

    def generate_token(self, expired: float = None, **kwargs) -> str:
        """生成token
        :param expired:过期时间,time.time()
        :return:token
        """
        if expired is not None:
            plugins.serializer.expires_in = expired

        info = {
            **kwargs
        }
        self.iat = time.time()
        info.update({'iat': self.iat})  # 记录更新时间
        result = plugins.serializer.dumps(info)  # 直接生成token
        return result.decode()  # bytes -> str 不然无法json

    def cache(self):
        """缓存用户信息"""

        info = self.user.serialization()
        info.update({'iat': self.iat})
        info = json.dumps(info)
        plugins.Redis.set(name=f'UserInfo_{self.user.uuid}', value=info)

    def get_cache(self, iat):
        """获取缓存"""

        result = plugins.Redis.get(name=f'UserInfo_{self.user.uuid}')
        if result is None:  # 验证缓存是否存在
            return False

        info = json.loads(result)  # 还原缓存信息
        if iat == info['iat']:  # 验证token 有效性
            return info
        else:
            return False
