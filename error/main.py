"""错误处理"""
from werkzeug.exceptions import HTTPException


class NeoException(HTTPException):
    """错误基类"""
    message = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999

    def __init__(self, error_code: int = None, code: int = 200, message='', **kwargs):
        if error_code:
            self.error_code = error_code
        self.code = code
        if message:
            self.message = message
        self.kwargs = kwargs

    @property
    def info(self):
        """请求相关信息"""
        return {'error_code': self.error_code, 'message': self.message, **self.kwargs}


class NotFound(NeoException):
    message = 'the resource are not found O__O...'
    error_code = 1004

    @property
    def info(self):
        """请求相关信息"""
        return {'error_code': self.error_code, 'message': self.message, **self.kwargs}
