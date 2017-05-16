from unittest import TestCase

from datetime import datetime

import geopic

class TestPicInfo(TestCase):

    def test_bad_file(self):
        pInfo = geopic.PicInfo("doesntexist.jpg")
        self.assertFalse(pInfo.isValid())

    def test_simple_construction(self):
        pInfo = geopic.PicInfo("./geopic/tests/pic_crete.jpg")
        self.assertTrue(pInfo.isValid())

    def test_dateTime_extraction(self):
        pInfo = geopic.PicInfo("./geopic/tests/pic_crete.jpg")
        expectedDateTime = datetime(2016, 9, 7, 13, 55, 34)
        self.assertTrue(expectedDateTime == pInfo.dateTime())

    def test_coordinate_extraction(self):
        pInfo = geopic.PicInfo("./geopic/tests/pic_crete.jpg")
        expectedCoordinates = (24.545555555555556, 35.12)
        self.assertTrue(expectedCoordinates == pInfo.coordinates())

    def test_location_extraction(self):
        pInfo = geopic.PicInfo("./geopic/tests/pic_crete.jpg")
        expectedLocation = geopic.Location(24.545555555555556, 35.12)
        self.assertTrue(expectedLocation == pInfo.location())

