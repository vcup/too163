import re
import api
import json
import data_sousa
import copy
import tools
import sqlite3


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


def spider_plid():
    """测试 database_add_playlist_song_id 的单元"""
    tools.databese_add_usr_playlist_id(2122797640)
    tools.databese_add_usr_playlist_id(1378240901)
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM user_playlist")
    for s in cursor.fetchall():
        print(s)


def spider_plsid():
    """测试 database_add_playlist_song_id 的单元"""
    tools.database_add_playlist_song_id(3207732903)
    tools.database_add_playlist_song_id(5003399521)
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM playlist_song")
    for s in cursor.fetchall():
        print(s)


def spider_plinfo():
    """database_add_usr_playlist_info"""
    tools.database_add_usr_playlist_info(2122797640)
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM playlist_info")
    for s in cursor.fetchall():
        print(s)



if __name__ == '__main__':
    for n in range(100):
        spider_plid()
        spider_plsid()
        spider_plinfo()
