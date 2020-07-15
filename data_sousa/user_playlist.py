class UserPlaylist:
    """解析来之 music.163.com/api/user/playlist 的数据"""

    def __init__(self, data: dict):
        self.path = key_path(data, point='playlist')
        self.len = len(self.path)
        self.more = data.get('more')

    def list(self, i: int = 0) -> dict:
        return self.path / f'[{i}]'

    def list_iter(self) -> Generator[dict, Any, None]:
        return (self.list(i) for i in range(self.len))
