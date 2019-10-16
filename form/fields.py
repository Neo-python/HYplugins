import wtforms
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
