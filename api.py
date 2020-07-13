import urllib3
import json


class RequestUrl:

    def __init__(self, url, headers=None, **urlopen_kw):
        self.url = url
        self.headers = headers
        self.http = urllib3.PoolManager()
        self.urlopen_kw = urlopen_kw

    def __get(self, mode: str, fields: dict, code: str) -> dict:
        while True:
            res = self.http.request(mode, self.url, fields, headers=self.headers, **self.urlopen_kw)
            if res.status == 200:
                return json.loads(res.data.decode(code))

    def get(self, code='UTF-8', **fields):
        return self.__get('get', fields, code)

    def post(self, code='UTF-8', **fields):
        return self.__get('POST', fields, code)


class SearchType:
    Song = 1
    Album = 10
    Artist = 100
    PlayList = 1000
    User = 1002
    MV = 1004
    Lyric = 1006
    Radio = 1009
    Video = 1014
    Comprehensive = 1018


api_url = 'https://127.0.0.1:3000'


def search(kw: str, res_type: int, limit: int, page: int = 0):
    res = RequestUrl(f'{api_url}/search')
    return res.post(keywords=kw, type=res_type, limit=limit, offset=page)


def lyric(sid: int, lrc: bool = True, tlrc: bool = True):
    parm = {'id': sid}
    res = RequestUrl(f'{api_url}/lyric')
    if lrc:
        parm.setdefault('lv', -1)
    if tlrc:
        parm.setdefault('tv', -1)
    return res.post(**parm)


def song(*sid: int):
    res = RequestUrl(f'{api_url}/song/detail')
    return res.post(ids=str(sid)[1:-1])


def playlist(pid: int):
    res = RequestUrl(f'{api_url}/playlist/detail')
    return res.post(id=pid)


def user(uid: int):
    res = RequestUrl(f'{api_url}/user/detail')
    return res.post(id=uid)


def user_playlist(uid: int, limit: int = 999999):
    res = RequestUrl(f'{api_url}/user/playlist')
    return res.post(uid=uid, limit=limit)


def album(album_id):
    res = RequestUrl(f'{api_url}/album')
    return res.post(id=album_id)


def artist(aid):
    res = RequestUrl(f'{api_url}/artists')
    return res.post(id=aid)


def artist_album(artist_id: int, limit: int = 2147483647):
    res = RequestUrl(f'{api_url}/artist/album')
    return res.post(id=artist_id, limit=limit)


def mv_url(mv_id: int):
    res = RequestUrl(f'{api_url}/mv/url')
    return res.post(id=mv_id)


def player_song(*ids: int, br: int = 2147483647):
    """提供多首歌的在线试听地址，无法获取无损但可以获取VIP歌曲地址"""
    res = RequestUrl(f'{api_url}/song/url')
    return res.post(ids=str(ids)[1:-1], br=br)


def download_file(sid: int, br: int = 2147483647):
    """提供单首歌的下载地址，可以获取无损但无法获取VIP歌曲(任何码率)"""
    res = RequestUrl('https://music.163.com/api/song/enhance/download/url')
    return res.post(id=sid, br=br)
