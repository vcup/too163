import datetime
import json
import time

from data_sousa import key_path
from data_sousa import song_detail
from typing import Union, Generator, Any, NewType

Url = NewType('Url', str)


class AlbumOld:

    def __init__(self, data: dict):
        self.path = key_path(data, point='album')
        self.len = len(self.path)

    def songs(self, i: int = 0) -> dict:
        """返回专辑的指定曲目"""
        return self.path / f'songs/[{i}]'

    def song_iter(self) -> Generator[song_detail, Any, None]:
        """迭代专辑包涵的所有曲目"""
        return (self.songs(i) for i in range((self.path / 'size') - 1))

    def artist(self) -> dict:
        """单个歌手信息，与self.artists不同"""
        return self.path / 'artist'

    def artists(self, i: int = 0) -> dict:
        """指定索引位置的歌手信息"""
        return self.path / f'artists/[{i}]'

    def artists_iter(self) -> Generator[dict, Any, None]:
        """迭代专辑的所有歌手信息"""
        return (self.artists(i) for i in range(self.path / 'artists'))

    def id(self) -> int:
        """专辑ID"""
        return self.path / 'id'

    def name(self) -> str:
        """专辑名"""
        return self.path / 'name'

    def pic_url(self) -> Url:
        """专辑的封面"""
        return self.path / 'picUrl'

    def size(self) -> int:
        """专辑包涵的曲目数"""
        return self.path / 'size'

    def info(self) -> dict:
        """奇怪信息"""
        return self.path / 'info'

    def pub_time(self) -> int:
        """发布时间的时间戳"""
        return self.path / 'publishTime'

    def pub_date(self, time_zone_info=None) -> datetime.datetime:
        """发布时间，返回datetime实例"""
        time_tuple = json.loads(
            time.strftime('[%Y, %m, %d, %H, %M, %S]',
                          time.localtime(self.pub_time())
                          )
        )
        return datetime.datetime(*time_tuple, tzinfo=time_zone_info)

    def company(self) -> str:
        """发行商"""
        return self.path / 'company'

    def desc(self) -> str:
        """简介"""
        return self.path / 'briefDesc'

    def tag(self) -> str:
        """标签"""
        return self.path / 'tags'

    def type(self) -> str:
        """专辑类型"""
        return self.path / 'type'

    def subtype(self) -> str:
        """子类型"""
        return self.path / 'subType'


class AlbumNew(AlbumOld):

    def songs(self, i: int = 0) -> dict:
        """返回专辑指定位置单曲"""
        return self.path.copy_set_point('') / f'songs/[{i}]'

    def song_iter(self) -> Generator[song_detail, Any, None]:
        """返回专辑所有单曲"""
        return (self.songs(i) for i in range((self.path / 'size') - 1))


def album(data: dict) -> Union[AlbumOld, AlbumNew]:
    if 'songs' in data.keys():
        return AlbumNew(data)
    return AlbumOld(data)
