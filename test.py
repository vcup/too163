import datetime
import time
import unittest
from json import loads

import test_item
from data_sousa import song, album, key_path


class TestDataSousa(unittest.TestCase):
    pass


class TestSong(TestDataSousa):
    @classmethod
    def setUpClass(cls) -> None:
        cls.song_dict_751472 = test_item.song_751472
        cls.song_dict_22808851 = test_item.song_22808851
        cls.song_dict_1293905025 = test_item.song_1293905025
        cls.song = song(cls.song_dict_751472, cls.song_dict_22808851, cls.song_dict_1293905025)

    def setUp(self) -> None:
        self.assertEqual('SongNew', self.song.__class__.__name__)

    def test_album(self):
        self.assertEqual(73747, self.song.album().get('id'))

    def test_album_iter(self):
        self.assertEqual([73747, 2096642, 71851620], [al.get('id') for al in self.song.album_iter()])

    def test_artist(self):
        self.assertEqual(16114, self.song.artist().get('id'))

    def test_artist_iter(self):
        self.assertEqual([16114], [ar.get('id') for ar in self.song.artist_iter()])

    def test_all_artist_iter(self):
        self.assertEqual([16114, 19780, 28083218], [ar.get('id') for ar in self.song.all_artist_iter()])

    def test_alia(self):
        self.assertEqual('琪露诺的完美算数教室', self.song.alia())
        
    def test_alias_iter(self):
        self.assertEqual(['琪露诺的完美算数教室'], list(self.song.alias_iter()))
    
    def test_all_alias_iter(self):
        self.assertEqual(['琪露诺的完美算数教室', 'TV动画《Happy Sugar Life》片头曲 / TVアニメ「ハッピーシュガーライフ」OPテーマ'],
                         list(self.song.all_alias_iter()))

    def test_name(self):
        self.assertEqual('チルノのパーフェクトさんすう教室', self.song.name())

    def test_name_iter(self):
        self.assertEqual(['チルノのパーフェクトさんすう教室', '物凄いあややがぶっちゃけ物凄いうた',
                          'ワンルームシュガーライフ (TV size ver.)'], list(self.song.name_iter()))

    def test_id(self):
        self.assertEqual(751472, self.song.id())

    def test_id_iter(self):
        self.assertEqual([751472, 22808851, 1293905025], list(self.song.id_iter()))

    def test_mvid(self):
        self.assertEqual(5326125, self.song.mvid())

    def test_mvid_iter(self):
        self.assertEqual([5326125, 0, 0], list(self.song.mvid_iter()))


class TestAlbum(TestDataSousa):

    @classmethod
    def setUpClass(cls) -> None:
        cls.album_dict = key_path(test_item.album_3308499)
        cls.album = album(cls.album_dict.data)

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
    unittest.main()
