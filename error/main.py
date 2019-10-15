"""错误处理"""


class ViewException(Exception):
    """view错误基类"""

    def __init__(self, error_code: int, message='', **kwargs):
        self.error_code = error_code
        self.message = message
        self.kwargs = kwargs

    @property
    def info(self):
        """请求相关信息"""
        return {'error_code': self.error_code, 'message': self.message, **self.kwargs}


class FormException(ViewException):
    """表单验证错误"""

    def __init__(self, error_code=1001, *args, **kwargs):
        super().__init__(error_code=error_code, *args, **kwargs)

    @property
    def info(self):
        """表单错误信息"""
        return {'error_code': self.error_code, 'message': self.message, **self.kwargs}


class NotFound(ViewException):
    message = 'the resource are not found O__O...'
    error_code = 1004

    @property
    def info(self):
        """请求相关信息"""
        return {'error_code': self.error_code, 'message': self.message, **self.kwargs}
