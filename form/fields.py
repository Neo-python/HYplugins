import wtforms
from wtforms.fields import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional, Regexp
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class OpenIdField:
    """微信open_id"""
    open_id = wtforms.StringField(validators=[DataRequired(message=VM.say('required', 'open_id'))])


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
        Length(min=24, max=24, message=VM.say('length_unite', '订单编号', 24))
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
