import logging

from pygeocoder import Geocoder, GeocoderError

class Location:

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
        self.valid = False

        try:
            self.geocoder_result = Geocoder.reverse_geocode(self.lat, self.lng)
        except GeocoderError as ge:
            logging.error("reverse_geocode for ({0},{1}) failed: '{2}'".format(self.lat, self.lng, ge))
            #TODO: CONSIDER: is this the best strategy here ?
            return

        if self.geocoder_result.count > 0:
            self.valid = True

    def isValid(self):
        return self.valid

    def country(self):
        """
        Return the country of a valid set of coordinates
        """
        if not self.isValid():
            return None
        return self.geocoder_result.country
