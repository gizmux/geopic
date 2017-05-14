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

    def test_localDateTime_extraction(self):
        pInfo = geopic.PicInfo("./geopic/tests/pic_crete.jpg")
        expectedDateTime = datetime(2016, 9, 7, 13, 55, 34)
        self.assertTrue(expectedDateTime == pInfo.localDateTime())

