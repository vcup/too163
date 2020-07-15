class Song:

    def __init__(self, *data: dict):
        new_songs = [s for ss in data for s in ss.get('songs')]
        try:
            data[0]['songs'] = new_songs
        except IndexError:
            raise TypeError(f'至少需要一个参数，传入了零个')
        self.path = key_path(data[0], point='songs')
        self.len = len(self.path)

    def album(self, i: int = 0) -> Album:
        """指定索引位置的歌曲的专辑信息"""
        return Album(self.path / f'[{i}]/al')

    def album_iter(self) -> Generator[Album, Any, None]:
        """迭代所有请求歌曲的专辑信息"""
        return (self.album(i) for i in range(self.len))

    def artist(self, i1: int = 0, i2: int = 0) -> Artist:
        """指定索引位置的歌曲的单个歌手信息"""
        return Artist(self.path / f'[{i1}]/ar/[{i2}]')

    def artist_iter(self, i1: int = 0) -> Generator[Artist, Any, None]:
        """迭代指定索引位置的歌曲的所有歌手信息"""
        return (self.artist(i1, i2) for i2 in range(len(self.path / f'[{i1}]/ar')))

    def all_artist_iter(self) -> Generator[List[Artist], Any, None]:
        """迭代所有请求歌曲的所有歌手信息"""
        return ([*self.artist_iter(i)] for i in range(self.len))

    def alia(self, i1: int = 0, i2: int = 0) -> str:
        """指定索引位置的歌曲的单个别名"""
        return self.path / f'[{i1}]/alia/[{i2}]'

    def alias_iter(self, i1: int = 0) -> Generator[str, Any, None]:
        """迭代指定索引位置的歌曲的所有别名"""
        return (self.alia(i1, i2) for i2 in range(len(self.path / f'[{i1}]/alia')))

    def all_alias_iter(self) -> Generator[list, Any, None]:
        """迭代所有请求歌曲的所有别名"""
        return ([*self.alias_iter(i)] for i in range(self.len))

    def name(self, i: int = 0) -> str:
        """指定索引位置的歌曲的名字"""
        return self.path / f'[{i}]/name'

    def name_iter(self) -> Generator[str, Any, None]:
        """迭代所有请求歌曲的名字"""
        return (self.name(i) for i in range(self.len))

    def id(self, i: int = 0) -> int:
        """指定索引位置的歌曲的ID"""
        return self.path / f'[{i}]/id'

    def id_iter(self) -> Generator[int, Any, None]:
        """迭代所有请求歌曲的ID"""
        return (self.id(i) for i in range(self.len))

    def mv(self, i: int = 0) -> int:
        """指定索引位置的歌曲的MV的ID"""
        return self.path / f'[{i}]/mv'

    def mv_iter(self) -> Generator[int, Any, None]:
        """迭代所有请求歌曲的MV的ID"""
        return (self.mv(i) for i in range(self.len))

    def album_no(self, i: int = 0) -> int:
        """返回指定位置单曲在所属专辑中的序号"""
        return self.path / f'[{i}]/no'

    def album_no_iter(self) -> Generator[int, Any, None]:
        """迭代请求歌曲在所属专辑中的序号"""
        return (self.album_no(i) for i in range(self.len))

    def pop(self, i: int = 0) -> int:
        """返回指定位置单曲的人气"""
        return self.path / f'[{i}]/pop'

    def pop_iter(self) -> Generator[int, Any, None]:
        """迭代请求所有歌曲的人气"""
        return (self.pop(i) for i in range(self.len))

    def duration(self, i: int = 0) -> int:
        """返回指定单曲的持续时间"""
        return self.path / f'[{i}]/dt'

    def duration_iter(self) -> Generator[int, Any, None]:
        """迭代请求歌曲的所有持续时间"""
        return (self.duration(i) for i in range(self.len))
