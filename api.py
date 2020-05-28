import urllib3
import json
from Crypto.Cipher import AES
import base64
import string, random
import binascii


class Net_Error(Exception):
    pass


class req_url:

    def __init__(self, parm: dict, headers: dict = None):
        self.http = urllib3.PoolManager(headers=headers)
        self.path = str(parm.pop(None)) if parm.get(None) else None
        parm_list = []
        for k, v in parm.items():
            parm_list.append(f'{k}={v}')
        self.parms = tuple(parm_list)

    def make_(self, url) -> str:
        if self.path:
            url = url + '/' if url[-1] != '/' else url  # if url last symbol not '/', add to
            url = (url + self.path) if self.path else url  # if self.path not None, add to
        if self.parms:
            url = url + '?' if url[-1] != '?' else url  # if url last symbol not '?', add to
        url += '&'.join(self.parms)  # add parm to url
        return url

    def __truediv__(self, url: str) -> urllib3.PoolManager.request:
        req = self.http.request('get', url=self.make_(url))
        count = 0
        while req.status != 200:
            count += 1
            if count > 10:
                raise Net_Error(f'Network GET Error Code:{req.status}')
            else:
                req = self.http.request('get', url=self.make_(url))
        return req

    __rtruediv__ = __truediv__
    set = __init__


class crypto_parm:

    def __init__(self):
        self.modulus = b'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa7' \
                       b'6d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46b' \
                       b'ee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = b'0CoJUm6Qyw8W8jud'
        self.pubKey = b'010001'
        self.iv = b'0102030405060708'
        self.pad = lambda s: ((s.decode('UTF-8') if isinstance(s, bytes) else s) + (16 - len(s) % 16) * chr(0)).encode('UTF-8')

    def AES_encrypto(self, text, key):
        text = self.pad(text)
        encrypto = AES.new(key, 2, self.iv)
        text = encrypto.encrypt(text)
        return base64.b64encode(text)

    def AES_decrypto(self, text, key):
        text = self.pad(text)
        encrypto = AES.new(key, 2, self.iv)
        text = base64.b64encode(text)
        return encrypto.decrypt(text)

    def RSA_encrypto(self):
        text = self.AES_key[::-1]
        rs = int(binascii.b2a_hex(text), 16)**int(self.pubKey, 16)%int(self.modulus, 16)
        return format(rs, 'x').zfill(256)

    def RSA_decrypto(self):
        """不会"""
        text = self.AES_key[::-1]

    def __call__(self, **parm) -> dict:
        self.parm = json.dumps(parm)
        self.AES_key = (''.join(random.sample(string.printable[:62], 16))).encode('UTF-8') # 随机生成16位由a-Z+0-9组成的字符串
        ciphertext = self.AES_encrypto(self.parm, self.nonce)
        return {'params': self.AES_encrypto(ciphertext, self.AES_key).decode('utf-8'), 'enSecKey': self.RSA_encrypto()}


def try_get_data(req: req_url, url: str) -> dict:
    req_obj = code = 0
    while code != 200:
        req_obj = req / url
        data = json.loads(req_obj.data.decode('UTF-8'))
        code = data.get('code')
        # print(data, '\n', req.make_(url)) # ; time.sleep(5.88)
    return json.loads(req_obj.data.decode('UTF-8'))


def resource(sid: int, limit: int, offset: int = 0):
    req = req_url({'limit': limit, 'offset': limit * offset})
    url = 'https://music.163.com/api/v1/resource/comments/R_SO_4_' + str(
        sid)
    return try_get_data(req, url)


def search(search_key: str, search_type: int, limit: int, offset: int = 0):
    # req = req_url({'s': search_key, 'type': search_type, 'limit': limit, 'offset': limit * offset})
    req = req_url({'keywords': search_key, 'type': search_type, 'limit': limit, 'offset': limit * offset})
    old_url = 'https://music.163.com/api/search/get/web'
    return try_get_data(req, 'http://localhost:3000/search?')


def lyric(sid: int, lrc: bool = True, tlrc: bool = True):
    parm = {'id': sid}
    if lrc:
        parm.setdefault('lv', -1)
    if tlrc:
        parm.setdefault('tv', -1)
    req = req_url(parm)
    old_url = 'https://music.163.com/api/song/lyric'
    return try_get_data(req, 'http://localhost:3000/lyric?')


def song_detail(sid: [int]):
    sid = sid if isinstance(sid, list) else [sid]
    req = req_url({'ids': ','.join(map(lambda i: str(i), sid))})
    old_url = 'https://music.163.com/api/song/detail''?ids=[id, id]'
    return try_get_data(req, 'http://localhost:3000/song/detail?')


def playlist(pid: int):
    req = req_url({'id': pid})
    old_url = 'https://music.163.com/api/playlist/detail'
    return try_get_data(req, 'http://localhost:3000/playlist/detail?')


def user(uid: int):
    req = req_url({None: uid})
    return try_get_data(req, 'https://music.163.com/api/v1/user/detail')


def user_playlist(uid: int, limit: int = 999999):
    req = req_url({'uid': uid, 'limit': limit})
    old_url = 'https://music.163.com/api/user/playlist'
    return try_get_data(req, 'http://localhost:3000/user/playlist')


def album(album_id):
    req = req_url({None: album_id})
    old_url = 'https://music.163.com/api/album'
    return try_get_data(req, 'https://music.163.com/api/album')


def artist(artist_id):
    req = req_url({None: artist_id})
    return try_get_data(req, 'https://music.163.com/api/artist')


def artist_album(artist_id: int):
    req = req_url({None: artist_id})
    return try_get_data(req, 'http://music.163.com/api/artist/albums')


def mv(mvid: int):
    req = req_url({'id': mvid, 'type': 'mp4'})
    return try_get_data(req, 'https://music.163.com/api/mv/detail')


def player_song(ids: [int], br: int = 2147483647):
    """提供多首歌的在线试听地址，无法获取无损但可以获取VIP歌曲地址"""
    ids = ids if isinstance(ids, list) else [ids]  # if ids is not list, convert to list
    req = req_url({'ids': ids, 'br': br})
    return try_get_data(req, 'https://music.163.com/api/song/enhance/player/url')


def download_file(sid: int, br: int = 2147483647):
    """提供单首歌的下载地址，可以获取无损但无法获取VIP歌曲(任何码率)"""
    req = req_url({'id': sid, 'br': br})
    return try_get_data(req, 'https://music.163.com/api/song/enhance/download/url')

