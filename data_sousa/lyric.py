from data_sousa import lyric_tools, KeyPath


class Lyric:

    def __init__(self, data: dict):
        self.path = KeyPath(data)

    def lrc(self) -> str:
        lrc_str = self.path.g('lrc/lyric')
        return lyric_tools.split_lrc(lrc_str if lrc_str else '')

    def tlrc(self) -> str:
        lrc_str = self.path.g('tlyric/lyric')
        return lyric_tools.split_lrc(lrc_str if lrc_str else '')

    def klrc(self) -> str:
        lrc_str = self.path.g('klyric/lyric')
        return lyric_tools.split_lrc(lrc_str if lrc_str else '')

    def lrc_plus(self) -> str:
        return lyric_tools.str_to_lyric(self.lrc(), self.tlrc())
