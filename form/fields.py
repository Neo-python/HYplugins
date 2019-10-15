import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional, Regexp
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class PhoneField:
    """手机"""
    phone = wtforms.StringField(validators=[
        Regexp('1\d{10}'),
        DataRequired(message=VM.say('required', '手机号')),
    ])


class CodeField:
    """验证码"""
    code = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '验证码')),
        Length(min=13, max=13, message=VM.say('length_unite', '验证码', 4))
    ]
    )
