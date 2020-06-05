import hashlib
import json, api
import data_sousa
import sqlite3
import check


def databese_add_usr_playlist_id(uid):
    """在 song_data 数据库文件中的 usr_playlist 表中添加数据
    表结构：user_id|playlist_id|list_type|hash(KEY)
    其中，list_type 是整数，0代表为常规歌单，用户自己创建的和用户收藏的；5代表歌单为用户的红心歌单"""
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM sqlite_master WHERE type='table' AND name = 'user_playlist'")
    if cursor.fetchall():
       usr_data = data_sousa.user_playlist(api.user_playlist(uid))
       for pl in usr_data.list_iter():
           pid = pl.get('id')
           ptype = pl.get('specialType')
           sha1 = hashlib.sha1(f'{uid}{pid}{ptype}'.encode('UTF-8')).hexdigest()
           cursor.execute(r"INSERT OR IGNORE INTO user_playlist VALUES (?, ?, ?, ?)", (uid, pid, ptype, sha1))
    else: # 如果表中没有user_playlist的表，则建立一个
        cursor.execute("""CREATE TABLE user_playlist (user_id int(16),
        playlist_id int(16),
        list_type int(1),
        hash char(40) PRIMARY KEY)""")

    conn.commit()
    cursor.close()
    conn.close()


def usr_all_play_list_gen(uid: int) -> iter:
    user_playlist_dict = api.user_playlist(uid)
    user_playlist = data_sousa.user_playlist(user_playlist_dict)
    return (data_sousa.playlist(play_list) for play_list in user_playlist.list_iter())


def play_list_all_song_info(pid: int) -> iter:
    play_list_dict = api.playlist(pid)
    play_list = data_sousa.playlist(play_list_dict)
    for sid in play_list.sid_iter():
        song_info = api.song_detail(sid)
        i = data_sousa.song_detail(song_info)
        yield {'name': i.name(), 'id': i.id(), 'artist': ','.join((x.get('name') for x in i.artist_iter()))}


def usr_all_song_info_of_playlist_gen(uid: int) -> iter:
    return (info_ for playlist in usr_all_play_list_gen(uid) for info_ in play_list_all_song_info(playlist.path / 'id'))


def dbis(uid):
    """把指定用户的所有歌曲加入数据库"""
    conn = sqlite3.connect('ids.db')
    cursor = conn.cursor()
    cursor.execute(r"select count(*) from sqlite_master where type='table' and name = 'user_all_song_list_id'")
    if cursor.fetchall() == [(0,)]: # 如果数据库中没有一个叫user_all_song_list_id的表，就创建一个
        cursor.execute(r"create table user_all_song_list_id (type varchar(4), id int(14) PRIMARY KEY, name varchar(255))")
    for s_info in usr_all_song_info_of_playlist_gen(uid):
        sid = s_info.get('id')
        name = s_info.get('name')
        artist = s_info.get('artist')
        print(f'{name} - {artist}')
        try:
            cursor.execute(r"INSERT INTO user_all_song_list_id VALUES ('song', ?, ?)", (sid, f'{name} - {artist}'))
        except sqlite3.IntegrityError as error:
            pass
    conn.commit()
    cursor.close()
    conn.close()


def g_lyric():
    """取出数据库中的所有歌曲ID，批量下载歌词"""
    conn = sqlite3.connect('ids.db')
    cursor = conn.cursor()
    cursor.execute(r"SELECT id, name FROM user_all_song_list_id WHERE type='song'")
    for sid, name in cursor.fetchall():
        lrc_data = api.lyric(sid)
        lrc_obj = data_sousa.lyric(lrc_data)
        lrc_str = lrc_obj.lrc_plus()
        if lrc_str:
            fn = check.format_fn(name)
            with open(f'lrc/{fn}.lrc', 'w', encoding='utf-8-sig') as file_obj:
                print(f'Size:{file_obj.write(lrc_str)}; {fn}')
        else:
            print(f'##Skip:{name}')


if __name__ == '__main__':
    #dbis(2122797640)
    #dbis(1378240901)
    #dbis(1595388977)
    #g_lyric()
    databese_add_usr_playlist_id(2122797640)
