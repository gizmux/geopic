from unittest import TestCase

import geopic

class TestLocate(TestCase):

	def test_invalid_coordinates(self):
		loc = geopic.Locate(99, 99999)
		self.assertFalse(loc.isValid())

	def test_country(self):
		loc = geopic.Locate(37.9709961, 23.6916685)
		self.assertTrue(loc.country() == "Greece")
