from data_sousa import key_path
from data_sousa import song_detail
from typing import Union, Generator, Any, NewType

Url = NewType('Url', str)


class album_old:

    def __init__(self, data: dict):
        self.path = key_path(data, point='album')
        self.len = len(self.path)


    def track(self, i: int = 0) -> dict:
        """返回专辑的指定曲目"""
        return self.path / f'songs/[{i}]'

    def track_iter(self) -> Generator[song_detail, Any, None]:
        """迭代专辑包涵的所有曲目"""
        return (self.track(i) for i in range(self.path / 'songs'))

    def artist(self) -> dict:
        """单个歌手信息，与self.aritsts不同"""
        return self.path / 'artist'

    def artists(self, i) -> dict:
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

    def picUrl(self) -> Url:
        """专辑的封面"""
        return self.path / 'picUrl'

    def size(self) -> int:
        """专辑包涵的曲目数"""
        return self.path / 'size'

    def info(self) -> dict:
        """奇怪信息"""
        return self.path / 'info'


class album_new(album_old):
    pass


def album(data: dict) -> Union[album_old, album_new]:
    return album_old(data)
