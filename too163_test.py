import re
import api
import json
import data_sousa
import copy


def key_path():
    data = {'k': {'0': '0w0', 0: {'': ['w'], 0: '"0"'}}, '': {'v': '-w-'}, '/': 'Nice!'}
    e = data_sousa.key_path(data)
    print(e / '')
    print(e / '/')
    print(e / 'k/0')
    print(e / 'k/[0]//')
    print(e / 'k/[0]/[0]')
    print(':P' if [s for s in e.return_values(('', 'k/[0]//[0]'))] == [e / '', e / 'k/[0]//[0]'] else ':L')
    print(e.copy_set_sep('|') / '/')


def index_path():
    data = ['-_-', '`-`', '=.=', {'v': ':]', '': ['\'.\'', 'Hey！'], '/': ':B'}]
    e = data_sousa.index_path(data)
    print(e / '')
    print(e / '3//')
    print(e / '0')
    print(e / '3')
    print(e / '3/[v]')
    print(e / '3//0')
    print([s for s in e.return_values(('3/[v]', '3//1'))])
    print(e.copy_set_sep('|') / '3|[/]')


def lyric_tools():
    lrc = '[00:00]www[00:00]vvv[00:00][00:00][00:00][00:00]l2'
    lrc_tuple = data_sousa.lyric_tools.split_lrc(lrc)
    lrc_dicts = map(data_sousa.lyric_tools.gen_time_line_dict, lrc_tuple.split('\n'))
    lrc_obj = data_sousa.lyric_tools.plus_lyric()
    lrc = ''
    for string in lrc_obj / lrc_dicts:
        lrc += string + '\n'
    print(lrc)




if __name__ == '__main__':
    lyric_tools()
