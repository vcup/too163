import unittest

import test_item
from data_sousa import song_detail, album


class TestDataSousa(unittest.TestCase):

    class TestSong(unittest.TestCase):
        @classmethod
        def setUpClass(cls) -> None:
            cls.song_dict_751472 = test_item.song_751472
            cls.song_dict_22808851 = test_item.song_22808851
            cls.song_dict_1293905025 = test_item.song_1293905025
            # cls.song = song_detail(cls.song_dict_751472, cls.song_dict_22808851, cls.song_dict_1293905025)
            cls.song_751472 = song_detail(cls.song_dict_751472)
            cls.song_22808851 = song_detail(cls.song_dict_22808851)
            cls.song_1293905025 = song_detail(cls.song_dict_1293905025)

    class TestAlbum(unittest.TestCase):

        @classmethod
        def setUpClass(cls) -> None:
            cls.album_dict = test_item.album_3308499
            cls.album = album(cls.album_dict)

        def test_songs(self):
            self.assertEqual('', self.album.songs())


if __name__ == '__main__':
    unittest.main()
