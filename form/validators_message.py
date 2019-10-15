messages = {
    'required': '{}是必须填写的,请填写后重试!',
    'required_select': '{}是必须选择的,请选择后重试!',
    'length': '{}的字符长度要求是:最少需要{}个字符,最多不超过{}个字符',
    'length_unite': '{}的字符长度为{}个字符'
}
system_message = {
    'system_number': '数值范围错误:{}-{}',
    'system_number_min': '数值最小值为:{}'
}

messages.update(system_message)


class ValidatorsMessage:

    @classmethod
    def say(cls, key, *args):
        """格式化消息"""
        content = messages.get(key, str())
        return content.format(*args)
