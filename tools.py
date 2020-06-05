import hashlib
import json, api
import data_sousa
import sqlite3
import check


def databese_add_usr_playlist_id(uid):
    """在 song_data.db 数据库文件中的 usr_playlist 表中添加数据
    表结构：uid|pid|list_type|hash(KEY)
    其中，list_type 是整数，0代表为常规歌单，用户自己创建的和用户收藏的；5代表歌单为用户的红心歌单"""
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM sqlite_master WHERE type='table' AND name = 'user_playlist'")
    if not cursor.fetchall():
        cursor.execute("""CREATE TABLE user_playlist (
        uid int(16),
        pid int(16),
        list_type int(1),
        hash char(40) PRIMARY KEY)""")

    usr_data = data_sousa.user_playlist(api.user_playlist(uid))
    for pl in usr_data.list_iter():
       pid = pl.get('id')
       ptype = pl.get('specialType')
       sha1 = hashlib.sha1(f'{uid}{pid}{ptype}'.encode('UTF-8')).hexdigest()
       cursor.execute(r"INSERT OR IGNORE INTO user_playlist VALUES (?, ?, ?, ?)", (uid, pid, ptype, sha1))

    conn.commit()
    cursor.close()
    conn.close()


def database_add_playlist_song_id(pid):
    """在 song_data.db 数据库文件中的 playlist_song 表中添加数据
    表结构：pid|sid|hash(KEY)"""
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM sqlite_master WHERE type='table' AND name = 'playlist_song'")
    if not cursor.fetchall():
        cursor.execute("""CREATE TABLE playlist_song (
        pid int(16),
        sid int(16),
        hash char(40) PRIMARY KEY)""")

    playlist_data = data_sousa.playlist(api.playlist(pid))
    for sid in playlist_data.sid_iter():
        sha1 = hashlib.sha1(f'{pid}{sid}'.encode('UTF-8')).hexdigest()
        cursor.execute(r"INSERT OR IGNORE INTO playlist_song VALUES (?, ?, ?)", (pid, sid, sha1))

    conn.commit()
    cursor.close()
    conn.close()


def database_add_usr_playlist_info(uid):
    """在 song_data.db 数据库文件中的 playlist_info 表中添加数据
    表结构：pid(KEY)|name|uid|size|hash
    由于歌单名字可能会变，所以不再以hash为主键，"""


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
    #databese_add_usr_playlist_id(2122797640)
    database_add_playlist_song_id(74069584)
