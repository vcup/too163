import datetime
import json
import time
from typing import Generator, Any

from data_sousa import KeyPath


class Album:

    def __init__(self, data: dict):
        self.path = KeyPath(data, point='album')
        self.len = len(self.path)

    def artist(self) -> KeyPath:
        """单个歌手信息，与self.artists不同"""
        return self.path.v('artist')

    def artists(self, i: int = 0) -> KeyPath:
        """指定索引位置的歌手信息"""
        return self.path.v(f'artists/[{i}]')

    def artists_iter(self) -> Generator[KeyPath, Any, None]:
        """迭代专辑的所有歌手信息"""
        return (self.artists(i) for i in range(len(self.path.get('artists'))))

    def id(self) -> KeyPath:
        """专辑ID"""
        return self.path.v('id')

    def name(self) -> KeyPath:
        """专辑名"""
        return self.path.v('name')

    def pic_url(self) -> KeyPath:
        """专辑的封面"""
        return self.path.v('picUrl')

    def size(self) -> KeyPath:
        """专辑包涵的曲目数"""
        return self.path.v('size')

    def info(self) -> KeyPath:
        """奇怪信息"""
        return self.path.v('info')

    def pub_time(self) -> KeyPath:
        """发布时间的时间戳"""
        return self.path.v('publishTime')

    def pub_date(self, time_zone_info=None) -> datetime.datetime:
        """发布时间，返回datetime实例"""
        time_tuple = json.loads(
            time.strftime('["%Y", "%m", "%d", "%H", "%M", "%S"]',
                          time.localtime(self.pub_time().data / 1000)
                          )
        )
        return datetime.datetime(*(int(n) for n in time_tuple), tzinfo=time_zone_info)

    def company(self) -> KeyPath:
        """发行商"""
        return self.path.v('company')

    def desc(self) -> KeyPath:
        """简介"""
        return self.path.v('briefDesc')

    def tag(self) -> KeyPath:
        """标签"""
        return self.path.v('tags')

    def type(self) -> KeyPath:
        """专辑类型"""
        return self.path.v('type')

    def subtype(self) -> KeyPath:
        """子类型"""
        return self.path.v('subType')

    def song(self, i: int = 0) -> KeyPath:
        """返回专辑指定位置单曲"""
        return self.path.copy_set_point('').v(f'songs/[{i}]')

    def song_iter(self) -> Generator['KeyPath', Any, None]:
        """返回专辑所有单曲"""
        return (self.song(i) for i in range(self.path.get('size').data))
