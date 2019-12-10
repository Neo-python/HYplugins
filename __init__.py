import config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

serializer = Serializer(secret_key=config.SECRET_KEY, expires_in=60 * 60 * 24 * 30)
