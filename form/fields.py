import config
import wtforms
import plugins
from wtforms.fields import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class WechatCodeField:
    """微信code"""
    wechat_code = wtforms.StringField(validators=[DataRequired(message=VM.say('required', 'wechat_code'))])

    def validate_wechat_code(self, *args):
        """验证微信code"""
        open_id = plugins.core_api.get_open_id(code=self.wechat_code.data, port=config.server_port)

        if open_id:
            self.open_id = open_id
        else:
            raise wtforms.ValidationError(message='微信码错误')


class PhoneField:
    """手机"""
    phone = wtforms.StringField(validators=[
        Regexp('1\d{10}', message='手机号错误,请检查手机号格式'),
        DataRequired(message=VM.say('required', '手机号')),
    ])


class CodeField:
    """验证码"""
    code = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '验证码')),
        Length(min=4, max=4, message=VM.say('length_unite', '验证码', 4))
    ]
    )


class OrderUuidField:
    """订单编号"""

    order_uuid = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '订单编号')),
        Length(min=12, max=12, message=VM.say('length_unite', '订单编号', 12))
    ]
    )


class UuidField:
    """厂家/驾驶员/管理员uuid"""

    uuid = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '用户唯一编号')),
        Length(min=32, max=32, message=VM.say('length_unite', '用户唯一编号', 32))
    ]
    )


class IdSortField:
    """按数据创建时间排序字段"""

    create_time_sort = IntegerField(validators=[
        Optional(),
        NumberRange(min=0, max=1, message=VM.say('system_number', 0, 1))
    ])
