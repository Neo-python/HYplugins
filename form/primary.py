import json
from flask import request
from flask_wtf import FlaskForm
from plugins.HYplugins.error import FormException
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM
from wtforms import widgets
from wtforms.compat import text_type
from wtforms import Field, ValidationError, IntegerField
from wtforms.validators import InputRequired as InputRequiredBase, StopValidation, NumberRange, DataRequired


class BaseForm(FlaskForm):
    """基础方法"""

    def validate_(self):
        """表单验证"""
        if request.method == 'GET':
            if self.validate() is False:
                raise FormException(error_code=1001, message=self.format_error(), error_fields=self.errors)
            else:
                return self
        else:
            if self.validate_on_submit() is False:
                raise FormException(error_code=1001, message=self.format_error(), error_fields=self.errors)
            else:
                return self

    def format_error(self):
        """格式化错误信息"""
        message = "表单填写错误,请检查."
        try:
            message = self.errors.popitem()[1][0]
        except Exception as err:
            print(err)
        return message


class StringField(Field):
    """
    This field is the base for most of the more complicated fields, and
    represents an ``<input type="text">``.
    """
    widget = widgets.TextInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0]
        elif self.data is None:
            self.data = self.default

    def _value(self):
        return text_type(self.data) if self.data is not None else self.default


class JsonField(Field):
    """验证json类型数据字段"""

    def process_formdata(self, value):
        """验证数据类型"""
        data = value
        if not isinstance(data, (dict, list)) and '[' not in data and '{' not in data:
            raise ValidationError('value to json error')
        if isinstance(data, (dict, list)):
            self.data = data
        else:
            try:
                self.data = json.loads(data)
            except BaseException:
                raise ValidationError('value to json error')


class InputRequired(InputRequiredBase):
    """修复输入0的bug"""

    def __call__(self, form, field):
        if not field.raw_data or (field.raw_data[0] is None or field.raw_data[0] is ''):
            if self.message is None:
                message = field.gettext('This field is required.')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)


class ListPage:
    """分页"""
    page = IntegerField(validators=[
        DataRequired(message=VM.say('required', '页码'))
    ],
        default=1
    )

    limit = IntegerField(validators=[
        NumberRange(min=1, max=50, message=VM.say('system_number', 1, 50))
    ],
        default=10
    )
