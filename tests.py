import datetime
import time
from json import loads
from unittest import TestCase, main

import test_item
from data_sousa import Song, Album, key_path


class TestDataSousa(TestCase):
    pass


class TestSong(TestDataSousa):

    @classmethod
    def setUpClass(cls) -> None:
        """测试用例存在耦合问题，期望输出被写死在方法内"""
        song_x3 = test_item.song_0, test_item.song_1, test_item.song_2
        cls.song = Song(*song_x3)
        cls.song_dict = key_path(test_item.song_3to1, point='songs')

    def setUp(self) -> None:
        self.assertEqual('Song', self.song.__class__.__name__)

    def gp(self, p: str):
        return (f'[{n}]/' + p for n in range(self.song.len))

    def test_init(self):
        self.assertRaisesRegex(TypeError, '至少需要一个参数，传入了零个',  self.song.__init__)

    def test_album(self):
        self.assertEqual(self.song_dict / '[0]/al/id', self.song.album().get('id'))

    def test_album_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('al'))],
                         [*self.song.album_iter()])

    def test_artist(self):
        self.assertEqual(self.song_dict / '[0]/ar/[0]/', self.song.artist())

    def test_artist_iter(self):
        self.assertEqual(self.song_dict / '[0]/ar', list(self.song.artist_iter()))

    def test_all_artist_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('ar'))],
                         [*self.song.all_artist_iter()])

    def test_alia(self):
        self.assertEqual(self.song_dict / '[0]/alia/[0]', self.song.alia())
        
    def test_alias_iter(self):
        self.assertEqual(self.song_dict / '[0]/alia', list(self.song.alias_iter()))
    
    def test_all_alias_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('alia'))],
                         [*self.song.all_alias_iter()])

    def test_name(self):
        self.assertEqual(self.song_dict / '[0]/name', self.song.name())

    def test_name_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('name'))],
                         [*self.song.name_iter()])

    def test_id(self):
        self.assertEqual(self.song_dict / '[0]/id', self.song.id())

    def test_id_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('id'))],
                         [*self.song.id_iter()])

    def test_mv(self):
        self.assertEqual(self.song_dict / '[0]/mv', self.song.mv())

    def test_mv_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('mv'))],
                         [*self.song.mv_iter()])

    def test_album_no(self):
        self.assertEqual(self.song_dict / '[0]/no', self.song.album_no())

    def test_album_no_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('no'))],
                         [*self.song.album_no_iter()])

    def test_duration(self):
        self.assertEqual(self.song_dict / '[0]/dt', self.song.duration())

    def test_duration_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('dt'))],
                         [*self.song.duration_iter()])


class TestAlbum(TestDataSousa):

    @classmethod
    def setUpClass(cls) -> None:
        cls.album_dict = key_path(test_item.album_3308499)
        cls.album = Album(cls.album_dict.data)

    def setUp(self) -> None:
        self.assertEqual('AlbumNew', self.album.__class__.__name__)

    def test_song_iter(self):
        songs = (s.get('id') for s in self.album_dict / 'songs')
        self.assertEqual(tuple(songs), tuple(s.get('id') for s in self.album.song_iter()))

    def test_artist(self):
        self.assertEqual(self.album_dict / 'album/artist', self.album.artist())

    def test_artists(self):
        self.assertEqual(self.album_dict / 'album/artists/[0]', self.album.artists())

    def test_artists_iter(self):
        artists = (a.get('id') for a in self.album_dict / 'album/artists')
        self.assertEqual(tuple(artists), tuple(a.get('id') for a in self.album.artists_iter()))

    def test_id(self):
        self.assertEqual(self.album_dict / 'album/id', self.album.id())

    def test_name(self):
        self.assertEqual(self.album_dict / 'album/name', self.album.name())

    def test_pic_url(self):
        self.assertEqual(self.album_dict / 'album/picUrl', self.album.pic_url())

    def test_pub_time(self):
        self.assertEqual(self.album_dict / 'album/publishTime', self.album.pub_time())

    def test_pub_date(self):
        """这个测试用例与测试的对象实现方法雷同"""
        time_zone_info = datetime.tzinfo()
        time_tuple = loads(
            time.strftime('["%Y", "%m", "%d", "%H", "%M", "%S"]',
                          time.localtime(self.album.pub_time() / 1000)
                          )
        )
        date = datetime.datetime(*(int(n) for n in time_tuple), tzinfo=time_zone_info)
        self.assertEqual(date, self.album.pub_date(time_zone_info))

    def test_company(self):
        self.assertEqual(self.album_dict / 'album/company', self.album.company())

    def test_desc(self):
        self.assertEqual(self.album_dict / 'album/briefDesc', self.album.desc())

    def test_tag(self):
        self.assertEqual(self.album_dict / 'album/tags', self.album.tag())

    def test_type(self):
        self.assertEqual(self.album_dict / 'album/type', self.album.type())

    def test_subtype(self):
        self.assertEqual(self.album_dict / 'album/subType', self.album.subtype())


if __name__ == '__main__':
    main()
