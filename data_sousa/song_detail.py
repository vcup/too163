from data_sousa import key_path
from typing import Union, Generator, Any


class song_detail_old:

    """解析来自 music.163.com/api/song/detail 的数据
    API一次返回多个歌曲的详细信息"""

    def __init__(self, data: dict):
        self.path = key_path(data, point='songs')
        self.len = len(self.path)

    def album(self, i: int = 0) -> dict:
        """指定索引位置的歌曲的专辑信息"""
        return self.path / f'[{i}]/album'

    def album_iter(self) -> Generator[dict, Any, None]:
        """迭代所有请求歌曲的专辑信息"""
        return (self.album(i) for i in range(self.len))

    def artist(self, i1: int = 0, i2: int = 0) -> dict:
        """指定索引位置的歌曲的单个歌手信息"""
        return self.path / f'[{i1}]/artists/[{i2}]'

    def artist_iter(self, i1: int = 0) -> Generator[dict, Any, None]:
        """迭代指定索引位置的歌曲的所有歌手信息"""
        return (self.artist(i1, i2) for i2 in range(len(self.path / f'[{i1}]/artists')))

    def all_aritst_iter(self) -> Generator[dict, Any, None]:
        """迭代所有请求歌曲的所有歌手信息"""
        return (a for i1 in range(self.len) for a in self.artist_iter(i1))

    def alias(self, i1: int = 0, i2: int = 0) -> str:
        """指定索引位置的歌曲的单个别名"""
        return self.path / f'[{i1}]/alias/[{i2}]'

    def alias_iter(self, i1: int = 0) -> Generator[str, Any, None]:
        """迭代指定索引位置的歌曲的所有别名"""
        return (self.alias(i1, i2) for i2 in range(len(self.path / f'[{i1}]/artists')))

    def all_alias_iter(self) -> Generator[dict, Any, None]:
        """迭代所有请求歌曲的所有别名"""
        return (a for i1 in range(self.len) for a in self.artist_iter(i1))

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

    def mvid(self, i: int = 0) -> int:
        """指定索引位置的歌曲的MV的ID"""
        return self.path / f'[{i}]/mvid'

    def mvid_iter(self) -> Generator[int, Any, None]:
        """迭代所有请求歌曲的MV的ID"""
        return (self.mvid(i) for i in range(self.len))


class song_detail_new(song_detail_old):
    """解析来自 music.163.com/weapi/v3/playlist/detail 的数据
    API一次返回多个歌曲的详细信息"""

    def album(self, i: int = 0) -> dict:
        """指定索引位置的歌曲的专辑信息"""
        return self.path / f'[{i}]/al'

    def album_iter(self) -> Generator[dict, Any, None]:
        """迭代所有请求歌曲的专辑信息"""
        return (self.album(i) for i in range(self.len))

    def artist(self, i1: int = 0, i2: int = 0) -> dict:
        """指定索引位置的歌曲的单个歌手信息"""
        return self.path / f'[{i1}]/ar/[{i2}]'

    def artist_iter(self, i1: int = 0) -> Generator[dict, Any, None]:
        """迭代指定索引位置的歌曲的所有歌手信息"""
        return (self.artist(i1, i2) for i2 in range(len(self.path / f'[{i1}]/ar')))

    def all_aritst_iter(self) -> Generator[dict, Any, None]:
        """迭代所有请求歌曲的所有歌手信息"""
        return (a for i1 in range(self.len) for a in self.artist_iter(i1))

    def alias(self, i1: int = 0, i2: int = 0) -> str:
        """指定索引位置的歌曲的单个别名"""
        return self.path / f'[{i1}]/alias/[{i2}]'

    def alias_iter(self, i1: int = 0) -> Generator[dict, Any, None]:
        """迭代指定索引位置的歌曲的所有别名"""
        return (self.artist(i1, i2) for i2 in range(len(self.path / f'[{i1}]/artists')))

    def all_alias_iter(self) -> Generator[dict, Any, None]:
        """迭代所有请求歌曲的所有别名"""
        return (a for i1 in range(self.len) for a in self.artist_iter(i1))

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

    def mvid(self, i: int = 0) -> int:
        """指定索引位置的歌曲的MV的ID"""
        return self.path / f'[{i}]/mv'

    def mvid_iter(self) -> Generator[int,Any, None]:
        """迭代所有请求歌曲的MV的ID"""
        return (self.mvid(i) for i in range(self.len))

    def picUrl(self, i: int = 0) -> int:
        """返回歌曲所属专辑的封面URL"""
        return self.path / f'[{i}]/al/picUrl'

    def picUrl_iter(self):
        """迭代所有请求歌曲所属专辑的封面URL"""
        return (self.picUrl(i) for i in range(self.len))

def song_detail(data: dict) -> Union[song_detail_old, song_detail_new]:
    """如果数据来自播放列表的'tracks'，把数据添加到一个新字典里包装起来避免出错;
    决定传入数据应该调用解析哪个版本的类"""
    if 'code' in data.keys(): # 直接调用API时返回的结果里必有'code'键
        return song_detail_new(data)
    data = {'privileges': None, 'songs': [data]}
    return song_detail_old(data)
