from unittest import TestCase

import geopic

class TestOrganize(TestCase):

    def test_init(self):
        org = geopic.Organize("./geopic")
        self.assertTrue(org.isValid())

    def test_simple_organize(self):
        org = geopic.Organize("./geopic")
        string = str(org)
        self.assertTrue(
            string.find("Netherlands") and
            string.find("Greece") and
            string.find("United Kingdom"))