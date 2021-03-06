import logging
from operator import itemgetter

#TODO: replace this with https://github.com/googlemaps/google-maps-services-python
from pygeocoder import Geocoder, GeocoderError

class Location:

    def __init__(self, lng, lat):
        self.lng        = lng
        self.lat        = lat
        self.valid      = False
        self._country   = None
        self._zones     = None
        try:
            #TODO: not a good idea to expose this publicly...
            geocoder = Geocoder(api_key="AIzaSyB-QYiv1mtdZKf0kMtX_u947Y-0rP_WB50")
            self.geocoder_results = geocoder.reverse_geocode(self.lat, self.lng)
        except GeocoderError as ge:
            logging.error("reverse_geocode for ({0},{1}) failed: '{2}'".format(
                self.lat, self.lng, ge))
            #TODO: CONSIDER: is this the best strategy here ?
            return
        if self.geocoder_results.count > 0:
            self.valid = True

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.lat == other.lat and self.lng == other.lng
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __str__(self):
        if not self.isValid():
            return "({0}, {1}) is an invalid location!".format(self.lng,
                self.lat)
        return "{0} ({1}, {2}) - ".format(self.country(), self.lng,
            self.lat) + str(self.zones())

    def isValid(self):
        return self.valid

    def country(self):
        """
        Return the country of a valid set of coordinates
        """
        if self._country is not None:
            return self._country
        if not self.isValid():
            return None
        self._country = self.geocoder_results.country
        return self._country

    def zones(self, limit=5):
        """
        Return a list of the Location zones from most general to most specific.
        Limit the depth of the search for zones to 'limit'
        """
        if self._zones is not None:
            return self._zones
        if not self.isValid():
            return None
        if not type(limit) is int:
            return None

        # First we extract all available zones up to the specified limit from
        # the reverse_geocode results
        temp_zones = dict()
        for datum in self.geocoder_results.data:
            for component in datum["address_components"]:
                for level in range(1, limit + 1):
                    zone_variable = "zone" + str(level)
                    admin_area_variable = ("administrative_area_level_" +
                        str(level))
                    if admin_area_variable in component["types"]:
                        admin_area = component["long_name"]
                        if zone_variable not in temp_zones:
                            temp_zones[zone_variable] = admin_area
                        elif temp_zones[zone_variable] != admin_area:
                            #TODO: perhaps raise an exception here ?
                            logging.warning(("'{0}' is inconsistent within the "
                                "reverse_geocode results: "
                                "'{1}' != '{2}'").format( admin_area_variable,
                                    temp_zones[zone_variable], admin_area))
                        continue
        # reset the results data object
        self.geocoder_results.current_index = 0

        # Now we create the list in general -> specific order
        self._zones = [ x for (k, x) in sorted(temp_zones.iteritems()) ]

        return self._zones
