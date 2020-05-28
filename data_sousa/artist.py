from data_sousa import key_path
from typing import Union, NewType, Generator, Any

Url = NewType('Url', str)


class artist_old:

    def __init__(self, data: dict):
        self.more = data.get('more')
        self.hot = data.get('hotSongs')
        self.path = key_path(data, point='artist')
        self.len = len(self.path)

    def alias(self, i: int = 0) -> str:
        return self.path / f'alias/[{i}]'

    def alias_iter(self) -> Generator[str, Any, None]:
        return (self.alias(i) for i in range(self.len))

    def picUrl(self) -> Url:
        return self.path / 'picUrl'

    def img(self) -> Url:
        """头像的原版尺寸"""
        return self.path / 'img1v1Url'

    def music_len(self) -> int:
        """歌手全部曲目数"""
        return self.path / 'musicSize'

    def album_len(self) -> int:
        """歌手全部专辑数"""
        return self.path / 'albumSize'

    def mv_len(self) -> int:
        """歌手全部mv数"""
        return self.path / 'mvSize'


def artist(data: dict) -> Union[artist_old]:
    return artist_old(data)
