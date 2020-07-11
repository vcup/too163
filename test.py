import unittest

import test_item
from data_sousa import album


class TestDataSousa(unittest.TestCase):

    class TestAlbum(unittest.TestCase):

        @classmethod
        def setUpClass(cls) -> None:
            cls.album = album(test_item.album_3308499)


if __name__ == '__main__':
    unittest.main()
