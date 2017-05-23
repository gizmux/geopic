from unittest import TestCase

import geopic

class TestLocation(TestCase):

    def test_invalid_coordinates(self):
        loc = geopic.Location(99, 99999)
        self.assertFalse(loc.isValid())

    def test_country(self):
        loc = geopic.Location(23.6916685, 37.9709961)
        self.assertTrue(loc.country() == "Greece")

    def test_zones(self):
        loc = geopic.Location(24.5955356, 35.1418955)
        self.assertTrue(loc.zones() == ["Crete Region", "Crete", "Rethimno", "Agios Vasileios", "Lampi"])
