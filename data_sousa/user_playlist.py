from data_sousa import key_path
from typing import Union, Generator, Any


class user_playlist_old:
    """解析来之 music.163.com/api/user/playlist 的数据"""

    def __init__(self, data: dict):
        self.path = key_path(data, point='playlist')
        self.len = len(self.path)
        self.more = data.get('more')

    def list(self, i: int = 0) -> dict:
        return self.path / f'[{i}]'

    def list_iter(self) -> Generator[dict, Any, None]:
        return (self.list(i) for i in range(self.len))


class user_playlist_new(user_playlist_old):
    pass


def user_playlist(data: dict) -> Union[user_playlist_old, user_playlist_new]:
    return user_playlist_old(data)
