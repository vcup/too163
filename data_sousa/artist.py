from data_sousa import key_path
from typing import Union


class artist_old:

    def __init__(self, data: dict):
        self.more = data.get('more')
        self.hot_songs = data.get('hotSongs')
        self.path = key_path(data, point='artist')
        self.len = len(self.path)


def artist(data: dict) -> Union[artist_old]:
    return artist_old(data)
