import unittest
import os
import igra


class DownloadTest(unittest.TestCase):
    def test_stationlist(self):
        # igra.download.stationlist('.')
        # self.assertTrue(os.path.isfile('./igrav2-staion-list.txt'))
        pass

    def test_station(self):
        # igra.download.station('USM00072216', '.')
        # self.assertTrue(os.path.isfile('./USM00072216-data.txt.zip'))
        pass

    def test_metadata(self):
        pass

    def test_update(self):
        pass


class ReadTest(unittest.TestCase):
    def test_stationlist(self):
        pass

    def test_station(self):
        pass

    def test_update(self):
        pass


class InterpTest(unittest.TestCase):
    def test_standard_pressure(self):
        self.assertFalse(False)

    def test_table(self):
        pass

    def test_custom_pressure(self):
        pass


if __name__ == '__main__':
    unittest.main()
