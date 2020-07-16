import copy
from json import dumps
from typing import Generator, Union, Any


class KeyPath:
    """如果希望使用数字作为索引的话，用任意的两个字符包在数字周围;
    直接使用空字符串作为路径，则返回self.data(除非设置了point)"""

    def __init__(self, data, sep: str = '/', point: str = '', back: int = 0):
        self.back = back
        self.point = point
        self.sep = sep
        self.data = data

    def set_back(self, back_value: int):
        """设置的back_value可以忽略指定级数的point(从末尾开始)"""
        self.back = back_value

    @property
    def meke_point(self) -> str:
        """self.back默认为0，str[:-0]会返回空字符串"""
        back_lever, self.back = self.back, 0  # 重置self.back
        point = self.split_path(self.point)
        if self.back != 0:
            return self.sep.join(point[:back_lever])  # 忽略指定级路径，同时用self.sep重新分隔成path
        return self.sep.join(point)  # 如果back为0，则不修改point

    def characters_inside_the_symbol(self, k: str) -> Union[str, int]:
        """尝试使用数字作为索引"""
        try:
            return int(k[1:-1])
        except ValueError:
            return k

    def get_value(self, paths: iter) -> 'KeyPath':
        """使用分隔后的路径迭代出路径指向的值"""
        data = self.data
        for key in paths:
            try:
                data = data[key]
            except (TypeError, KeyError, IndexError) as error:
                if isinstance(error, TypeError):
                    error_type = TypeError
                elif isinstance(error, KeyError):
                    error_type = KeyError
                else:
                    error_type = IndexError
                raise error_type(
                    f'{error}    \n    key: {key}, data: {data.keys() if isinstance(data, dict) else data}'
                )
        return self.copy(data)

    def split_path(self, path: str = None):
        """用设置的分隔符切割传入的path，如果path空则切割self.path"""
        path = path if path else self.path
        if path:
            if path[-1] == self.sep:  # 删除多出来的空字符串 '/k1/k2//'.split('/') -> ['', 'k1', 'k2', '', '']
                return path.split(self.sep)[:-1]
            return path.split(self.sep)
        else:
            return ''

    def __truediv__(self, path: str) -> 'KeyPath':
        """用真除魔法除以路径返回对应值; 设置了point会在point后接续路径"""
        self.path = f'{self.meke_point}{self.sep}{path}' if self.point else path
        # paths = map(self.characters_inside_the_symbol, self.split_path())
        paths = [self.characters_inside_the_symbol(k) for k in self.split_path()]
        return self.get_value(paths)

    def return_values(self, *paths: str, **kwargs: str) -> Generator['KeyPath', Any, None]:
        """返回多个路径对应的值"""
        for path in paths:
            res = self.__truediv__(path)
            yield getattr(res, kwargs.get('attr'), res)

    def get(self, path):
        """模仿dict.get方法"""
        try:
            return self.__truediv__(path)
        except (KeyError, IndexError):
            return None

    def get_iter(self, paths) -> iter:
        return (self.get(path) for path in paths)

    set = __init__

    def set_point(self, point: str):
        self.set(data=self.data, point=point, sep=self.sep)

    def set_sep(self, sep: str):
        self.set(data=self.data, sep=sep, point=self.point)

    def set_data(self, data):
        self.set(data=data, sep=self.sep, point=self.point)

    def copy(self, *args, **kwargs):
        """不修改实例属性的情况下返回另一个修改特定属性的实例;
        引用此方法的同理"""
        self_ = copy.copy(self)
        self_.set(*args, **kwargs)
        return self_

    def copy_set_point(self, point):
        return self.copy(data=self.data, point=point, sep=self.sep)

    def copy_set_sep(self, sep: str):
        return self.copy(data=self.data, sep=sep, point=self.point)

    def copy_set_data(self, data):
        return self.copy(data=data, sep=self.sep, point=self.point)

    def __len__(self):
        return len(self.__truediv__('').data)

    def __str__(self):
        return dumps(self.data)


class IndexPath(KeyPath):
    """如果希望使用字符串作为索引的话，用任意的两个字符包在数字周围;
        直接使用空字符串作为路径，则返回data(除非设置了point)"""

    def characters_inside_the_symbol(self, k: str) -> int or str:
        """尝试使用字符串作为索引"""
        try:
            return int(k)
        except ValueError:
            return k[1:-1]
