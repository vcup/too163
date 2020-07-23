import json, api
import data_sousa
import sqlite3
import check


def usr_all_play_list_gen(uid: int) -> iter:
    user_playlist_dict = api.user_playlist(uid)
    user_playlist = data_sousa.user_playlist(user_playlist_dict)
    return (data_sousa.playlist(play_list) for play_list in user_playlist.list_iter())


def play_list_all_song_info(pid: int) -> iter:
    play_list_dict = api.playlist(pid)
    play_list = data_sousa.playlist(play_list_dict)
    for sid in play_list.sid_iter():
        song_info = api.song(sid)
        i = data_sousa.Song(song_info)
        yield {'name': i.name(), 'id': i.id(), 'artist': ','.join((x.g('name') for x in i.artist_iter()))}


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
        lrc_obj = data_sousa.Lyric(lrc_data)
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
    g_lyric()
