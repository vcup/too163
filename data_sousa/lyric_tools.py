import re
import data_sousa
from typing import AnyStr


class split_lrc_c:

    def __init__(self, *rules):
        self.rules = rules

    def replace_str_gen(self, rules: tuple) -> iter:
        for rule in rules:
            for Match in re.finditer(rule, self.lrc_str):
                replace_str = Match.group()
                yield replace_str
                self.buffer.add(replace_str)

    def __call__(self, *lrc_strings: str) -> str:
        lrc_str = ''
        for s in lrc_strings:
            lrc_str += s
        self.lrc_str = lrc_str.replace('\n', '')
        self.buffer = set()
        for rs in self.replace_str_gen(self.rules):
            nrs = '\n' + rs
            self.lrc_str = self.lrc_str if rs in self.buffer else self.lrc_str.replace(rs, nrs)
        return self.lrc_str


def split_lrc(*args: str) -> str:
    return split_lrc_c(r'\[[^\d]+?:[^\d]+?\]',
                       r'\[\d+?[.|:]\d+?\]',
                       r'\[\d+?[.|:]\d+?[.|:]\d+?\]',
                       r'\[\d+?[.|:]\d+?\]')(*args)


def gen_time_line_dict(lrc: str) -> dict:
    time_line = re.match(r'\[[^\d]+?:[^\d]+?\]|\[\d+?[.|:]\d+?\]|\[\d+?[.|:]\d+?[.|:]\d+?\]', lrc)
    time_line = time_line.group() if time_line else ''
    text = lrc.replace(time_line, '')  # remove time_line
    return {time_line: text}


class plus_lyric:

    def __init__(self, split: str = '  //  '):
        self.split = split
        self.buffer = set()
        self.lrc_list = []
        self.dict = {}

    @property
    def tl(self):
        return tuple(self.dict.keys())[0]

    @property
    def text(self):
        return self.dict.get(self.tl)

    def tl_in_buffer(self, tl: str = None):
        """检查传入的时间轴是否在缓存中，如果不在则添加并返回False"""
        tl = tl if tl else self.tl
        if tl in self.buffer:
            return True
        self.buffer.add(self.tl)
        return False

    def add_tl(self):
        """self.lrc_list的结构是 [(tl, [text1, text2]), ...]。第一个元素是时间轴，第二个是歌词正文的列表
        如果时轴对于的歌词正文为空，则不做任何检查直接添加到self.lrc_list；否则
        迭代self.lrc_list中的全部tuple，如果tuple的时轴与调用此方法时的self.tl相同，
        把此次调用时的歌词正文添加到歌词正文的列表"""
        tl = self.tl
        text = self.text
        if text:
            tl_text: tuple = [x for x in self.lrc_list if x[0] == tl][0] # 列表只会生成一个元素
            index: int = self.lrc_list.index(tl_text) # 获取匹配的tuple在列表中的索引
            tl_text[1].append(self.text) # 添加正文到列表中
            self.lrc_list[index] = tl_text # 应用修改
        else:
            self.lrc_list.append((tl, []))

    def return_and_clear(self):
        """由于使用了类的属性来储存歌词条目和已经遇到的时轴，在调用结束的时候需要清空"""
        lrc_list = self.lrc_list.copy()
        self.lrc_list.clear(); self.buffer.clear()
        return (tl + self.split.join(texts) for tl, texts in lrc_list) # 用预设的分隔符连接歌词正文

    def __truediv__(self, lrc_dicts: iter):
        for self.dict in lrc_dicts:
            if self.tl_in_buffer():
                self.add_tl()
            else:
                self.lrc_list.append((self.tl, [self.text]))
        return self.return_and_clear()


def str_to_lyric(*lrc_str: AnyStr, **kwargs):
    """kwargs只能使用split，其他参数名会报错
    例: str_to_lyric('lrc_str1', lrc_str2, split=r'  \\  ')"""
    lyric = lyric_str = ''
    lrc_gen = plus_lyric(**kwargs)
    for s in lrc_str:
        lyric_str += split_lrc(s)
    for lrc in lrc_gen / map(gen_time_line_dict, lyric_str.split('\n')):
        lyric += lrc + '\n'
    return lyric[1:] if lyric[0] == '\n' else lyric
