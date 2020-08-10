import datetime
import time
from json import loads
from unittest import TestCase, main

import test_item
from data_sousa import KeyPath
from data_sousa.song import Song
from data_sousa.album import Album
from data_sousa.artist import Artist, ArtistMv, ArtistAlbum


# 测试data_sousa模块: {{{
class TestDataSousa(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def gp(self, p: str, k: KeyPath, path_kw: dict, **kwargs):
        """字符串 p 必须是可以被 path_kw 格式化的字符串，例：
        data: [{'!': ''}, ...]
        p: '[{n}]/{ww}'
        path_kw: {'ww': '!'}
        return: '[0]/!', ...
        """
        if kwargs:
            k = k.copy(**kwargs)
        i = p.index('[{n}]')
        for n in range(len(k.v(p[:i].format(**path_kw)))):
            path_kw['n'] = n
            yield p.format(**path_kw)


class TestSong(TestDataSousa):

    @classmethod
    def setUpClass(cls) -> None:
        super(TestSong, cls).setUpClass()
        song_x3 = test_item.song_0, test_item.song_1, test_item.song_2
        cls.song = Song(*song_x3)
        cls.song_K = KeyPath(test_item.song_3to1, point='songs')

    def setUp(self) -> None:
        self.assertEqual('Song', self.song.__class__.__name__)

    def gp(self, p, **kwargs):
        return super(TestSong, self).gp('[{n}]/{p}', self.song_K, {'p': p, 'n': 0}, **kwargs)

    def test_init(self):
        self.assertRaisesRegex(TypeError, '至少需要一个参数，传入了零个', self.song.__init__)

    def test_album(self):
        self.assertEqual(self.song_K.v('[0]/al'), self.song.album())

    def test_album_iter(self):
        self.assertEqual([*self.song_K.vs(*self.gp('al'))],
                         [album for album in self.song.album_iter()])

    def test_artist(self):
        self.assertEqual(self.song_K.v('[0]/ar/[0]'), self.song.artist())

    def test_artist_iter(self):
        self.assertEqual(self.song_K.v('[0]/ar'),
                         [artist for artist in self.song.artist_iter()])

    def test_all_artist_iter(self):
        self.assertEqual([*self.song_K.vs(*self.gp('ar'))],
                         [[a for a in artist] for artist in self.song.all_artist_iter()])

    def test_alia(self):
        self.assertEqual(self.song_K.v('[0]/alia/[0]'),
                         self.song.alia())

    def test_alias_iter(self):
        self.assertEqual(self.song_K.v('[0]/alia'),
                         [alia for alia in self.song.alias_iter()])

    def test_all_alias_iter(self):
        self.assertEqual([*self.song_K.vs(*self.gp('alia'))],
                         [[alia for alia in alias] for alias in self.song.all_alias_iter()])

    def test_name(self):
        self.assertEqual(self.song_K.v('[0]/name'), self.song.name())

    def test_name_iter(self):
        self.assertEqual([*self.song_K.vs(*self.gp('name'))],
                         [name for name in self.song.name_iter()])

    def test_id(self):
        self.assertEqual(self.song_K.v('[0]/id'), self.song.id())

    def test_id_iter(self):
        self.assertEqual([*self.song_K.vs(*self.gp('id'))],
                         [sid for sid in self.song.id_iter()])

    def test_mv(self):
        self.assertEqual(self.song_K.v('[0]/mv'), self.song.mv())

    def test_mv_iter(self):
        for a, b in zip(self.song_K.vs(*self.gp('mv')), self.song.mv_iter()):
            self.assertEqual(a.data, b.data)

    def test_album_no(self):
        self.assertEqual(self.song_K.v('[0]/no'), self.song.album_no())

    def test_album_no_iter(self):
        self.assertEqual([*self.song_K.vs(*self.gp('no'))],
                         [album_no for album_no in self.song.album_no_iter()])

    def test_duration(self):
        self.assertEqual(self.song_K.v('[0]/dt'), self.song.duration())

    def test_duration_iter(self):
        self.assertEqual([*self.song_K.vs(*self.gp('dt'))],
                         [duration for duration in self.song.duration_iter()])


class TestAlbum(TestDataSousa):

    @classmethod
    def setUpClass(cls) -> None:
        super(TestAlbum, cls).setUpClass()
        cls.album_K = KeyPath(test_item.album_3308499)
        cls.album = Album(cls.album_K.data)

    def setUp(self) -> None:
        self.assertEqual('Album', self.album.__class__.__name__)

    def gp(self, p, **kwargs):
        return super(TestAlbum, self).gp('{p}/[{n}]', self.album_K, {'p': p}, **kwargs)

    def test_song(self):
        self.assertEqual(self.album_K.v('songs/[0]'), self.album.song())

    def test_song_iter(self):
        self.assertEqual([*self.album_K.vs(*self.gp('songs'), attr='data')],
                         [album for album in self.album.song_iter()])

    def test_artist(self):
        self.assertEqual(self.album_K.v('album/artist'), self.album.artist())

    def test_artists(self):
        self.assertEqual(self.album_K.v('album/artists/[0]'), self.album.artists())

    def test_artists_iter(self):
        for a, b in zip(self.album_K.vs(*self.gp('album/artists')), self.album.artists_iter()):
            self.assertEqual(a.data, b.data)

    def test_id(self):
        self.assertEqual(self.album_K.v('album/id'), self.album.id())

    def test_name(self):
        self.assertEqual(self.album_K.v('album/name'), self.album.name())

    def test_pic_url(self):
        self.assertEqual(self.album_K.v('album/picUrl'), self.album.pic_url())

    def test_pub_time(self):
        self.assertEqual(self.album_K.v('album/publishTime'),
                         self.album.pub_time())

    def test_pub_date(self):
        """这个测试用例与测试的对象实现方法雷同"""
        time_zone_info = datetime.tzinfo()
        time_tuple = loads(
            time.strftime('["%Y", "%m", "%d", "%H", "%M", "%S"]',
                          time.localtime(self.album.pub_time().data / 1000)
                          )
        )
        date = datetime.datetime(*(int(n) for n in time_tuple), tzinfo=time_zone_info)
        self.assertEqual(date, self.album.pub_date(time_zone_info))

    def test_company(self):
        self.assertEqual(self.album_K.v('album/company'), self.album.company())

    def test_desc(self):
        self.assertEqual(self.album_K.v('album/briefDesc'), self.album.desc())

    def test_tag(self):
        self.assertEqual(self.album_K.v('album/tags'), self.album.tag())

    def test_type(self):
        self.assertEqual(self.album_K.v('album/type'), self.album.type())

    def test_subtype(self):
        self.assertEqual(self.album_K.v('album/subType'), self.album.subtype())


class TestArtist(TestDataSousa):

    @classmethod
    def setUpClass(cls) -> None:
        super(TestArtist, cls).setUpClass()
        cls.artist_K = KeyPath(test_item.artist_160442, point='artist')
        cls.artist_album_K = KeyPath(test_item.artist_album_160442)
        cls.artist = Artist(cls.artist_K.data)
        cls.artist_album = ArtistAlbum(cls.artist_album_K.data)

    def setUp(self) -> None:
        self.assertEqual('Artist', self.artist.__class__.__name__)

    def gp(self, p, **kwargs):
        return super(TestArtist, self).gp('{p}/[{n}]', self.artist_K, {'p': p}, **kwargs)

    def test_alia(self):
        self.assertEqual(self.artist_K.v('trans'), self.artist.alia())

    def test_alias(self):
        self.assertEqual(self.artist_K.v('alias/[0]'), self.artist.alias())

    def test_alias_iter(self):
        self.assertEqual([*self.artist_K.vs(*self.gp('alias'))], [*self.artist.alias_iter()])

    def test_desc(self):
        self.assertEqual(self.artist_K.v('briefDesc'), self.artist.desc())

    def test_name(self):
        self.assertEqual(self.artist_K.v('name'), self.artist.name())

    def test_id(self):
        self.assertEqual(self.artist_K.v('id'), self.artist.id())

    def test_pic(self):
        self.assertEqual(self.artist_K.v('picUrl'), self.artist.pic())

    def test_img(self):
        self.assertEqual(self.artist_K.v('img1v1Url'), self.artist.img())

    def test_music_len(self):
        self.assertEqual(self.artist_K.v('musicSize'), self.artist.music_len())

    def test_album_len(self):
        self.assertEqual(self.artist_K.v('albumSize'), self.artist.album_len())

    def test_mv_len(self):
        self.assertEqual(self.artist_K.v('mvSize'), self.artist.mv_len())

    def test_song(self):
        self.assertEqual(self.artist_K.cs_point('').v('hotSongs/[0]'), self.artist.song())

    def test_song_iter(self):
        for a, b in zip(self.artist_K.copy(self.artist_K.data, point='').vs(
                *self.gp('hotSongs', data=self.artist_K.data, point='')
        ), self.artist.song_iter()):
            self.assertEqual(a.data, b.data)


class TestArtistAlbum(TestArtist):

    @classmethod
    def setUpClass(cls):
        cls.album_d = KeyPath(test_item.artist_album_160442)
        cls.album = ArtistAlbum(cls.album_d.data)

    def setUp(self):
        self.assertEqual('ArtistAlbum', self.album.__class__.__name__)

    def gp(self, p, **kwargs):
        return super(TestArtist, self).gp('{p}/[{n}]', self.artist_album_K, {'p': p}, **kwargs)

    def test_album(self):
        self.assertEqual(self.album_d.v('hotAlbums/[0]'), self.album.album())

    def test_album_iter(self):
        for a, b in zip(self.album_d.vs(*self.gp('hotAlbums')), self.album.album_iter()):
            self.assertEqual(a.data, b.data)


class TestArtistMv(TestDataSousa):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artist_mv_K = KeyPath(test_item.artist_mv_28083218)
        cls.artist_mv = ArtistMv(cls.artist_mv_K.data)

    def setUp(self) -> None:
        super().setUp()

    def gp(self, p, **kwargs):
        return super(TestArtistMv, self).gp('{p}/[{n}]', self.artist_mv_K, {'p': p}, **kwargs)

    def test_mv(self):
        self.assertEqual(self.artist_mv_K.v('mvs/[0]'), self.artist_mv.mv())

    def test_mv_iter(self):
        for a, b in zip(self.artist_mv_K.vs(*self.gp('mvs')), self.artist_mv.mv_iter()):
            self.assertEqual(a.data, b.data)


# }}}


if __name__ == '__main__':
    main()
