import datetime
import time
from json import loads
from unittest import TestCase, main

import test_item
from data_sousa import Song, Album, KeyPath


class TestDataSousa(TestCase):
    pass


class TestSong(TestDataSousa):

    @classmethod
    def setUpClass(cls) -> None:
        song_x3 = test_item.song_0, test_item.song_1, test_item.song_2
        cls.song = Song(*song_x3)
        cls.song_dict = KeyPath(test_item.song_3to1, point='songs')

    def setUp(self) -> None:
        self.assertEqual('Song', self.song.__class__.__name__)

    def gp(self, p: str):
        return (f'[{n}]/' + p for n in range(self.song.len))

    def test_init(self):
        self.assertRaisesRegex(TypeError, '至少需要一个参数，传入了零个', self.song.__init__)

    def test_album(self):
        self.assertEqual(self.song_dict.get('[0]/al/id').data, self.song.album().get('id').data)

    def test_album_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('al'), attr='data')],
                         [album.data for album in self.song.album_iter()])

    def test_artist(self):
        self.assertEqual(self.song_dict.get('[0]/ar/[0]').data, self.song.artist().data)

    def test_artist_iter(self):
        self.assertEqual(self.song_dict.get('[0]/ar').data,
                         [artist.data for artist in self.song.artist_iter()])

    def test_all_artist_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('ar'), attr='data')],
                         [[a.data for a in artist] for artist in self.song.all_artist_iter()])

    def test_alia(self):
        self.assertEqual(self.song_dict.get('[0]/alia/[0]').data,
                         self.song.alia().data)

    def test_alias_iter(self):
        self.assertEqual(self.song_dict.get('[0]/alia').data,
                         [alia.data for alia in self.song.alias_iter()])

    def test_all_alias_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('alia'), attr='data')],
                         [[alia.data for alia in alias] for alias in self.song.all_alias_iter()])

    def test_name(self):
        self.assertEqual(self.song_dict.get('[0]/name').data, self.song.name().data)

    def test_name_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('name'), attr='data')],
                         [name.data for name in self.song.name_iter()])

    def test_id(self):
        self.assertEqual(self.song_dict.get('[0]/id').data, self.song.id().data)

    def test_id_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('id'), attr='data')],
                         [sid.data for sid in self.song.id_iter()])

    def test_mv(self):
        self.assertEqual(self.song_dict.get('[0]/mv').data, self.song.mv().data)

    def test_mv_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('mv'), attr='data')],
                         [mv.data for mv in self.song.mv_iter()])

    def test_album_no(self):
        self.assertEqual(self.song_dict.get('[0]/no').data, self.song.album_no().data)

    def test_album_no_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('no'), attr='data')],
                         [album_no.data for album_no in self.song.album_no_iter()])

    def test_duration(self):
        self.assertEqual(self.song_dict.get('[0]/dt').data, self.song.duration().data)

    def test_duration_iter(self):
        self.assertEqual([*self.song_dict.return_values(*self.gp('dt'), attr='data')],
                         [duration.data for duration in self.song.duration_iter()])


class TestAlbum(TestDataSousa):

    @classmethod
    def setUpClass(cls) -> None:
        cls.album_dict = KeyPath(test_item.album_3308499)
        cls.album = Album(cls.album_dict.data)

    def setUp(self) -> None:
        self.assertEqual('Album', self.album.__class__.__name__)

    def gp(self, p: str):
        n: int = len(self.album_dict.get(p).data)
        return (p + f'/[{n}]' for n in range(n))

    def test_song(self):
        self.assertEqual(self.album_dict.get('songs/[0]').data, self.album.song().data)

    def test_song_iter(self):
        self.assertEqual([*self.album_dict.return_values(*self.gp('songs'), attr='data')],
                         [album.data for album in self.album.song_iter()])

    def test_artist(self):
        self.assertEqual(self.album_dict.get('album/artist').data, self.album.artist().data)

    def test_artists(self):
        self.assertEqual(self.album_dict.get('album/artists/[0]').data, self.album.artists().data)

    def test_artists_iter(self):
        self.assertEqual([*self.album_dict.return_values(*self.gp('album/artists'), attr='data')],
                         [artist.data for artist in self.album.artists_iter()])

    def test_id(self):
        self.assertEqual(self.album_dict.get('album/id').data, self.album.id().data)

    def test_name(self):
        self.assertEqual(self.album_dict.get('album/name').data, self.album.name().data)

    def test_pic_url(self):
        self.assertEqual(self.album_dict.get('album/picUrl').data, self.album.pic_url().data)

    def test_pub_time(self):
        self.assertEqual(self.album_dict.get('album/publishTime').data,
                         self.album.pub_time().data)

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
        self.assertEqual(self.album_dict.get('album/company').data, self.album.company().data)

    def test_desc(self):
        self.assertEqual(self.album_dict.get('album/briefDesc').data, self.album.desc().data)

    def test_tag(self):
        self.assertEqual(self.album_dict.get('album/tags').data, self.album.tag().data)

    def test_type(self):
        self.assertEqual(self.album_dict.get('album/type').data, self.album.type().data)

    def test_subtype(self):
        self.assertEqual(self.album_dict.get('album/subType').data, self.album.subtype().data)


if __name__ == '__main__':
    main()
