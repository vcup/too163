from typing import Generator, Any

from data_sousa import KeyPath


class Artist:

    def __init__(self, data: dict):
        self.more = data.get('more')
        self.hot = data.get('hotSongs')
        self.path = KeyPath(data, point='artist')
        self.len = len(self.path)

    def alias(self, i: int = 0) -> KeyPath:
        return self.path.v(f'alias/[{i}]')

    def alias_iter(self) -> Generator[KeyPath, Any, None]:
        return (self.alias(i) for i in range(self.len))

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
