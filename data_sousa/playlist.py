from typing import Generator, Any

from data_sousa import KeyPath


class Playlist:

    def __init__(self, data):
        self.path = KeyPath(data, point='playlist')
        self.len = len(self.path)

    def song_ids(self, i: int = 0) -> KeyPath:
        """歌单中指定位置的歌曲的一些信息"""
        return self.path / f'trackIds/[{i}]'

    def song_ids_iter(self) -> Generator[KeyPath, Any, None]:
        """迭代歌单中包含的的全部歌曲的信息"""
        tracks_len = len(self.path / 'trackIds')
        return (self.song_ids(i) for i in range(tracks_len))

    def privileges(self, i: int = 0) -> KeyPath:
        """歌单中指定位置的歌曲的一些信息，最多十个"""
        self.path.set_back(1)
        return self.path / f'privileges/[{i}]'

    def privileges_iter(self) -> Generator[KeyPath, Any, None]:
        tracks_len = int(self.path / 'privileges')
        return (self.privileges(i) for i in range(tracks_len))

    def sid(self, i: int = 0) -> int:
        """歌单中指定位置的歌曲id"""
        return self.song_ids(i).get('id')

    def sid_iter(self) -> Generator[int, Any, None]:
        """迭代歌单中全部歌曲的id"""
        return (s.get('id') for s in self.song_ids_iter())

    def track(self, i: int = 0) -> KeyPath:
        return self.path / f'tracks/[{i}]'

    def track_iter(self) -> Generator[KeyPath, Any, None]:
        tracks_len = len(self.path / 'tracks')
        return (self.track(i) for i in range(tracks_len))

    def name(self, i: int = 0) -> str:
        return self.track(i).get('id')

    def name_iter(self) -> Generator[str, Any, None]:
        return (s.get('name') for s in self.track_iter())
