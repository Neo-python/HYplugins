"""系统/管理员后台类短信功能"""
from models.HYModels.system import Admin


class SystemSms:
    """系统短信"""

    def __init__(self, sms):
        self.sms = sms

    def broadcast(self):
        """通知管理员"""
