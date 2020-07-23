from datetime import datetime
from functools import partial
from typing import Generator, Any

from data_sousa import KeyPath
from data_sousa.sousa_tool import timestamp


class Artist:

    def __init__(self, data: dict):
        self.more = data.get('more')
        self.path = KeyPath(data, point='artist')
        self.len = len(self.path)

    def alia(self) -> KeyPath:
        return self.path.v('trans')

    def alias(self, i: int = 0) -> KeyPath:
        return self.path.v(f'alias/[{i}]')

    def alias_iter(self) -> Generator[KeyPath, Any, None]:
        return (self.alias(i) for i in range(len(self.path.v('alias'))))

    def desc(self) -> KeyPath:
        return self.path.v('briefDesc')

    def name(self) -> KeyPath:
        return self.path.v('name')

    def id(self):
        return self.path.v('id')

    def pic(self) -> KeyPath:
        return self.path.v('picUrl')

    def img(self) -> KeyPath:
        """头像的原版尺寸"""
        return self.path.v('img1v1Url')

    def music_len(self) -> KeyPath:
        """歌手全部曲目数"""
        return self.path.v('musicSize')

    def album_len(self) -> KeyPath:
        """歌手全部专辑数"""
        return self.path.v('albumSize')

    def mv_len(self) -> KeyPath:
        """歌手全部mv数"""
        return self.path.v('mvSize')

    def song(self, i: int = 0) -> KeyPath:
        return self.path.cs_point('').v(f'hotSongs/[{i}]')

    def song_iter(self) -> Generator[KeyPath, Any, None]:
        return (self.song(i) for i in range(len(self.path.v('hotSong'))))


class ArtistAlbum(Artist):

    def album(self, i: int = 0) -> KeyPath:
        path = self.path.cs_point('')
        return path.v(f'hotAlbums/{i}')

    def album_iter(self) -> Generator[KeyPath, Any, None]:
        return (self.album(i) for i in range(len(self.album_len())))


class ArtistMv:

    def __init__(self, data: dict):
        self.path = KeyPath(data)
        self.path.v = partial(self.path.v)
        self.len = len(data.get('mvs'))
        self.more = data.get('hasMore')

    def mv(self, i: int = 0) -> KeyPath:
        return self.path.v(f'mvs/{i}')

    def mv_iter(self) -> Generator[KeyPath, Any, None]:
        return (self.mv(i) for i in range(self.len))

    def time(self) -> datetime:
        return timestamp(self.path.v('time', attr='data'))
