from unittest import TestCase

import geopic

class TestOrganize(TestCase):

    def test_init(self):
        org = geopic.Organize("./geopic")
        self.assertTrue(org.isValid())