import json
from flask import request
from flask_wtf import FlaskForm
from plugins.HYplugins.error import FormException
from wtforms import widgets
from wtforms.compat import text_type
from wtforms import Field, ValidationError
from wtforms.validators import InputRequired as InputRequiredBase, StopValidation, NumberRange, DataRequired


class BaseForm(FlaskForm):
    """基础方法"""

    def validate_(self):
        """表单验证"""
        if request.method == 'GET':
            if self.validate() is False:
                raise FormException(error_code=1001, message='请求参数错误.', error_fields=self.errors)
            else:
                return self
        else:
            if self.validate_on_submit() is False:
                raise FormException(error_code=1001, message='请求参数错误.', error_fields=self.errors)
            else:
                return self


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
