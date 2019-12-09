import os
import unittest
from datetime import datetime

import pandas as pd
import xarray as xr

import igra

tmpdir = '/tmp/igra-test'


class DownloadTest(unittest.TestCase):
    def test_stationlist(self):
        test = igra.download.stationlist(tmpdir)
        self.assertTrue(os.path.isfile('%s/igra2-station-list.txt' % tmpdir))

    def test_station(self):
        igra.download.station('USM00072216', tmpdir)
        self.assertTrue(os.path.isfile('%s/USM00072216-data.txt.zip' % tmpdir))

    def test_metadata(self):
        igra.download.metadata(tmpdir)
        self.assertTrue(os.path.isfile('%s/igra2-metadata.txt' % tmpdir))

    def test_update(self):
        iyear = str(datetime.now().year - 1)
        igra.download.update('USM00072216', tmpdir, year=iyear)
        self.assertTrue(os.path.isfile('%s/USM00072216-data-beg%s.txt.zip' % (tmpdir, iyear)))


class ReadTest(unittest.TestCase):
    def test_stationlist_nofile(self):
        with self.assertRaises(IOError):
            data = igra.read.stationlist('')

    def test_stationlist(self):
        data = igra.read.stationlist('%s/igra2-station-list.txt' % tmpdir)
        self.assertIsInstance(data, pd.DataFrame)

    def test_station(self):
        data, station = igra.read.igra('USM00072216', '%s/USM00072216-data.txt.zip' % tmpdir)
        self.assertIsInstance(data, xr.Dataset) and self.assertIsInstance(station, xr.Dataset)

    def test_station_ascii(self):
        data, station = igra.read.ascii_to_dataframe('%s/USM00072216-data.txt.zip' % tmpdir)
        self.assertIsInstance(data, pd.DataFrame) and self.assertIsInstance(station, pd.DataFrame)

    def test_station_table(self):
        data, station = igra.read.igra('USM00072216', '%s/USM00072216-data.txt.zip' % tmpdir, return_table=True)
        self.assertIsInstance(data, xr.Dataset) and self.assertIsInstance(station, xr.Dataset)

    def test_metadata(self):
        data = igra.read.metadata('%s/igra2-metadata.txt' % tmpdir)
        self.assertIsInstance(data, pd.DataFrame)

    def test_update(self):
        pass


# todo add Interpolation test
class InterpTest(unittest.TestCase):
    def test_standard_pressure(self):
        self.assertFalse(False)

    def test_table(self):
        pass

    def test_custom_pressure(self):
        pass

    def test_interpolation(self):
        pass


if __name__ == '__main__':
    unittest.main()
    if os.path.isdir(tmpdir):
        os.removedirs(tmpdir)
