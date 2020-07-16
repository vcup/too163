from typing import Generator, Any

from data_sousa import KeyPath


class UserPlaylist:
    """解析来之 music.163.com/api/user/playlist 的数据"""

    def __init__(self, data: dict):
        self.path = KeyPath(data, point='playlist')
        self.len = len(self.path)
        self.more = data.get('more')

    def list(self, i: int = 0) -> KeyPath:
        return self.path / f'[{i}]'

    def list_iter(self) -> Generator[KeyPath, Any, None]:
        return (self.list(i) for i in range(self.len))
