from unittest import TestCase

import geopic

class TestPicInfo(TestCase):

    def test_bad_file(self):
        pInfo = geopic.PicInfo("doesntexist.jpg")
        self.assertFalse(pInfo.isValid())

    def test_gps_europe(self):
        pInfo = geopic.PicInfo("./geopic/tests/pic_crete.jpg")
        self.assertTrue(pInfo.isValid())

