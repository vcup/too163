from data_sousa import key_path
from data_sousa import song_detail
from data_sousa import artist
from typing import Union


class album_old:

    def __init__(self, data: dict):
        self.path = key_path(data, point='album')
        self.len = len(self.path)


    def track(self, i: int = 0):
        """返回专辑的指定曲目"""
        return song_detail(self.path / f'songs/[{i}]')

    def track_iter(self):
        """迭代专辑包涵的所有曲目"""
        return (self.track(i) for i in range(self.path / 'songs'))

    def artist(self):
        """单个歌手信息，与self.aritsts不同"""
        return artist(self.path / 'artist')

    def artists(self, i):
        """指定索引位置的歌手信息"""
        return artist(self.path / f'artists/[{i}]')

    def artists_iter(self):
        """迭代专辑的所有歌手信息"""
        return (self.artists(i) for i in range(self.path / 'artists'))

    def id(self):
        """专辑ID"""
        return self.path / 'id'

    def name(self):
        """专辑名"""
        return self.path / 'name'

    def picUrl(self):
        """专辑的封面"""
        return self.path / 'picUrl'

    def size(self):
        """专辑包涵的曲目数"""
        return self.path / 'size'

    def info(self):
        """"""
        return self.path / 'info'


class album_new(album_old):
    pass


def album(data: dict) -> Union[album_old, album_new]:
    return album_old(data)
