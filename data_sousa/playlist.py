from typing import Union

from data_sousa import key_path


class playlist_old:

    def __init__(self, data: dict):
        self.path = key_path(data, point='result')
        self.len = len(self.path)

    def track(self, i: int = 0) -> dict:
        return self.path / f'tracks/[{i}]'

    def track_iter(self) -> iter:
        tracks_len = len(self.path / 'tracks')
        return (self.track(i) for i in range(tracks_len))

    def sid(self, i: int = 0):
        return self.track(i).get('id')

    def sid_iter(self):
        return (s.get('id') for s in self.track_iter())

    def name(self, i: int = 0):
        return self.track(i).get('id')

    def name_iter(self):
        return (s.get('name') for s in self.track_iter())


class playlist_new(playlist_old):

    def trackIds(self, i: int = 0) -> dict:
        return self.path / f'trackIds/[{i}]'

    def trackIds_iter(self) -> trackIds:
        tracks_len = len(self.path / 'trackIds')
        return (self.trackIds(i) for i in range(tracks_len))

    def privileges(self, i: int = 0 ) -> dict:
        self.path.set_back(1)
        return self.path / f'privileges/[{i}]'

    def privileges_iter(self) -> privileges:
        tracks_len = (self.path / 'privileges')
        return (self.privileges(i) for i in range(tracks_len))

    def sid(self, i: int = 0):
        return self.trackIds(i).get('id')

    def sid_iter(self):
        return (s.get('id') for s in self.trackIds_iter())


def playlist(data: dict) -> Union[playlist_new, playlist_old]:
    if data.get('privileges'):
        return playlist_new(data)
    else:
        if 'tracks' in data.keys():
            data = {'!!':'old', 'result':data}
        return playlist_old(data)
