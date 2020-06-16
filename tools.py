import api
import data_sousa
import sqlite3
import check


def databese_add_usr_playlist_id(uid):
    """在 song_data.db 数据库文件中的 usr_playlist 表中添加数据
    表结构：uid|pid|list_type
    其中，list_type 是整数，0代表为常规歌单，用户自己创建的和用户收藏的；5代表歌单为用户的红心歌单"""
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM sqlite_master WHERE type='table' AND name = 'user_playlist'")
    if not cursor.fetchall():
        cursor.execute("""CREATE TABLE user_playlist (
        uid int(16),
        pid int(16),
        list_type int(1)
        )""")

    usr_data = data_sousa.user_playlist(api.user_playlist(uid))
    for pl in usr_data.list_iter():
        pid = pl.get('id')
        ptype = pl.get('specialType')
        cursor.execute(r"INSERT OR IGNORE INTO user_playlist VALUES (?, ?, ?)", (uid, pid, ptype))

    conn.commit()
    cursor.close()
    conn.close()


def database_add_playlist_song_id(pid):
    """在 song_data.db 数据库文件中的 playlist_song 表中添加数据
    表结构：pid|sid"""
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM sqlite_master WHERE type='table' AND name = 'playlist_song'")
    if not cursor.fetchall():
        cursor.execute("""CREATE TABLE playlist_song (
        pid int(16),
        sid int(16)
        )""")

    playlist_data = data_sousa.playlist(api.playlist(pid))
    for sid in playlist_data.sid_iter():
        cursor.execute(r"INSERT OR IGNORE INTO playlist_song VALUES (?, ?)", (pid, sid))

    conn.commit()
    cursor.close()
    conn.close()


def database_add_usr_playlist_info(uid):
    """在 song_data.db 数据库文件中的 playlist_info 表中添加数据
    表结构：pid(KEY)|name|uid|intro(简介)|picUrl
    由于歌单名字可能会变，所以不再以hash为主键"""
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM sqlite_master WHERE type='table' AND name = 'playlist_info'")
    if not cursor.fetchall():
        cursor.execute("""CREATE TABLE playlist_info (
        pid int(16) PRIMARY KEY,
        name varchar(40),
        uid int(16),
        intro varchar(1000),
        picUrl varchar(100)
        )""")

    usr_playlist = data_sousa.user_playlist(api.user_playlist(uid))
    for pl in usr_playlist.list_iter():
        pid = pl.get('id')
        name = pl.get('name')
        intro = pl.get('description')
        picUrl = pl.get('coverImgUrl')
        if len(name) > 40 or len(intro) > 1000 or len(picUrl) > 100:
            raise ValueError(f'长度错误：name:{len(name)} intro:{len(intro)} picUrl:{len(picUrl)}')

        cursor.execute(r"INSERT OR IGNORE INTO playlist_info VALUES (?, ?, ?, ?, ?)", (
            pid, name, uid, intro, picUrl))

    conn.commit()
    cursor.close()
    conn.close()


def database_add_playlist_song_info(sid):
    """在 song_data.db 数据库文件中的 song_info 表中添加数据
    表结构：sid|name|album_id|artist_ids|alias(别名)|picUrl|mvid
    artist_ids 是 varchar，格式为artist_id/artist_id/...
    alias 同 artist_ids"""
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()

    cursor.execute(r"SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'song_info'")
    if not cursor.fetchall():
        cursor.execute("""CREATE TABLE song_info (
        sid int(16),
        name varchar(255),
        album_id int(16),
        artist_ids varchar(255),
        alias varchar(255),
        picUrl varchar(100),
        mvid int(16)
        )""")

    song_detail = data_sousa.song_detail(api.song_detail(sid))
    info = (song_detail.id_iter(), song_detail.name_iter(), song_detail.album_iter(),
            song_detail.artist_iter(),
            song_detail.alias_iter(), song_detail.picUrl_iter(), song_detail.mvid_iter())
    for sid, name, album_id, artist_ids, alias, picUrl, mvid in zip(info):
        if len(name) > 255 or len(artist_ids) > 255 or len(alias) > 255 or len(picUrl) > 100:
            raise ValueError(f'长度错误：name:{len(name)} artist_ids:{len(artist_ids)} alias:{len(alias)} picUrl:{picUrl}')

        cursor.execute(r"INSERT OR IGNORE INTO song_info (?, ?, ?, ?, ?, ?, ?)",
                       (sid, name, album_id, artist_ids, alias, picUrl, mvid))

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
    #databese_add_usr_playlist_id(2122797640)
    database_add_playlist_song_id(74069584)
