from unittest import TestCase

import geopic

class TestLocation(TestCase):

	def test_invalid_coordinates(self):
		loc = geopic.Location(99, 99999)
		self.assertFalse(loc.isValid())

	def test_country(self):
		loc = geopic.Location(37.9709961, 23.6916685)
		self.assertTrue(loc.country() == "Greece")
