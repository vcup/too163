import copy
from typing import Any, Dict, Generator, Iterator, List, Union


class KeyPath:
    """初始化时传入list或dict作为必选参数，然后调用对应方法获取其中的值
    sep是分隔路径用的符号，默认时'/'
    point是路径的基准点，设置之后调用方法获取值会在路径前面加上
    up_path_bol是上一层路径的标识符，默认为'..'，遇到该符号则在该符号前面一个路径重新开始
    attr是最后获取的数据的期望属性，调用方法时传入会被覆盖"""

    def __init__(self, data: Union[List, Dict],
                 sep: str = '/', point: str = '', up_path_bol: str = '..', attr: str = ''):
        self.data = data
        self.sep = sep
        self.point = point
        self.up = up_path_bol
        self.attr = attr

    def copy(self, data: Union[List, Dict], **kwargs) -> 'KeyPath':
        self_copy = copy.copy(self)
        self_copy.__init__(data, **kwargs)
        return self_copy

    def split_path(self, path: str) -> Iterator[Union[int, str]]:
        """对传入的path切割，并在前面加上point切割后的部分"""
        key_list = self.point.split(self.sep) + path.split(self.sep)
        try:
            index = key_list.index(self.up)
            del key_list[index-1:index+1]
        except ValueError:
            pass
        return [self.try_num(key) for key in key_list]

    def try_num(self, key: str) -> Union[int, str]:
        """尝试将key变成int"""
        try:
            return int(key[1:-1])
        except ValueError:
            return key

    def value(self, key_list: iter) -> 'KeyPath':
        """获取路径对应的值"""
        data = self.data
        for key in key_list:
            try:
                data = data[key]
            except KeyError:
                if key == '':
                    continue
        return self.copy(data)

    def v(self, path: str, attr: str = '') -> 'KeyPath':
        """返回point+path使用sep切割后，对应的data中的值
        如果有value的key为数字，则用任意字符将数字括起来"""
        attr = attr if attr else self.attr
        res = self.value(self.split_path(path))
        return getattr(res, attr, None if attr else res)

    def vs(self, *paths: str, **kwargs) -> Generator['KeyPath', None, Any]:
        """获取多个路径对应的值"""
        return (self.v(path, **kwargs) for path in paths)

    def g(self, path: str, **kwargs) -> Union['KeyPath', None]:
        """获取路径对应的值而不抛出错误"""
        try:
            return self.v(path, **kwargs)
        except (KeyError, IndexError):
            return None

    def gs(self, *paths: str, **kwargs) -> Generator['KeyPath', None, Any]:
        """获取多个路径对应的值而不抛出错误"""
        return (self.g(path, **kwargs) for path in paths)

    set = __init__

    def set_point(self, point: str):
        self.set(data=self.data, point=point, sep=self.sep)

    def set_sep(self, sep: str):
        self.set(data=self.data, sep=sep, point=self.point)

    def set_data(self, data):
        self.set(data=data, sep=self.sep, point=self.point)

    def cs_point(self, point) -> 'KeyPath':
        return self.copy(data=self.data, point=point, sep=self.sep)

    def cs_sep(self, sep: str) -> 'KeyPath':
        return self.copy(data=self.data, sep=sep, point=self.point)

    def cs_data(self, data) -> 'KeyPath':
        return self.copy(data=data, sep=self.sep, point=self.point)

    def __len__(self) -> int:
        return len(self.data)

    def __int__(self) -> int:
        return int(self.data)

    def __eq__(self, value: Union[Dict, List]) -> bool:
        return self.data == value


class IndexPath(KeyPath):
    """如果希望使用字符串作为索引的话，用任意的两个字符包在数字周围;
        直接使用空字符串作为路径，则返回data(除非设置了point)"""

    def try_num(self, key):
        """尝试使用字符串作为索引"""
        try:
            return int(key)
        except ValueError:
            return key[1:-1]
