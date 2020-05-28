from data_sousa import lyric_tools
from data_sousa import key_path
from typing import Union


class lyric_old:

    def __init__(self, data: dict):
        self.path = key_path(data)
        self.len = len(self.path)

    def lrc(self) -> str:
        lrc_str = self.path.get('lrc/lyric')
        return lyric_tools.split_lrc(lrc_str if lrc_str else '')

    def tlrc(self) -> str:
        lrc_str = self.path.get('tlyric/lyric')
        return lyric_tools.split_lrc(lrc_str if lrc_str else '')

    def lrc_plus(self) -> str:
        return lyric_tools.str_to_lyric(self.lrc(), self.tlrc(), split=r'  \\  ')


class lyric_new(lyric_old):

    def tlrc(self) -> str:
        lrc_str = self.path.get('tlyric/lyric')
        return lyric_tools.split_lrc(lrc_str if lrc_str else '')

    def klrc(self) -> str:
        lrc_str = self.path.get('klyric/lyric')
        return lyric_tools.split_lrc(lrc_str if lrc_str else '')

    def lrc_plus(self) -> str:
        return lyric_tools.str_to_lyric(self.lrc(), self.tlrc())


def lyric(data: dict) -> Union[lyric_old, lyric_new]:
    if data.get('klyric'): # 新API调用结果里有 klyric 键
        return lyric_new(data)
    else:
        return lyric_old(data)