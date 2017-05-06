import logging
from operator import itemgetter

from pygeocoder import Geocoder, GeocoderError

class Location:

    def __init__(self, lat, lng):
        self.lat        = lat
        self.lng        = lng
        self.valid      = False
        self._country   = None
        self._zones     = None
        try:
            self.geocoder_results = Geocoder.reverse_geocode(self.lat, self.lng)
        except GeocoderError as ge:
            logging.error("reverse_geocode for ({0},{1}) failed: '{2}'".format(
                self.lat, self.lng, ge))
            #TODO: CONSIDER: is this the best strategy here ?
            return
        if self.geocoder_results.count > 0:
            self.valid = True

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
