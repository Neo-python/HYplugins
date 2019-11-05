"""百度位置相关功能"""
import requests
import json
import config
from plugins.HYplugins.error import ViewException


class Position:
    """api对象"""

    distance_url = 'http://api.map.baidu.com/routematrix/v2/driving'

    def __init__(self, key: str, coord_type: str = 'gcj02', tactics: int = 13):
        self.key = key
        self.coord_type = coord_type
        self.tactics = tactics

    def distance(self, origin: str, destinations: list):
        """计算距离与耗时"""
        origins = origin
        destinations = '|'.join(destinations)
        params = {
            'origins': origins,
            'destinations': destinations,
            'coord_type': self.coord_type,
            'tactics': self.tactics, 'ak': self.key
        }
        result = requests.get(url=self.distance_url, params=params)
        result = json.loads(result.content)
        if result['status'] == 0:
            return result['result']
        else:
            print(result)
            raise ViewException(error_code=4007, message='position api error')


position = Position(key=config.POSITION_APP_KEY)

# import itertools
#
# a, b = [1, 2, 3], [4, 5, 6]
# print(list(itertools.product(a, b)))
# _ = {'status': 0, 'result': [{'distance': {'text': '5.3公里', 'value': 5343}, 'duration': {'text': '3分钟', 'value': 200}},
#                              {'distance': {'text': '8.4公里', 'value': 8400}, 'duration': {'text': '5分钟', 'value': 314}}],
#      'message': '成功'}
