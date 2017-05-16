import logging
from datetime import datetime

import exifread

from .location import Location

class PicInfo:
    """
    Class for retrieving and parsing info stored within picture files.
    Currently supports parsing exif tags via the exifread module.
    """

    def __init__(self, picFileName):
        self.picFileName    = picFileName
        self.valid          = False
        self.tags           = None
        self._datetime      = None
        self._location      = None
        self._coordinates   = (None, None)
        try:
            with open(picFileName, 'rb') as f:
                self.tags = exifread.process_file(f, details=False)
        except IOError as e:
            logging.error("Unable to open '{0}' because '{1}'".format(
                picFileName, e))
            #TODO: CONSIDER: is this the best strategy here ?
            return
        if self.tags is not None:
            self.valid = True

    def isValid(self):
        return self.valid

    def dateTime(self):
        """
        Return a dateTime object representig the date and time the picture
        was taken. This is in the local timzone of the location that the
        picture was taken.
        """
        if self._datetime is not None:
            return self._datetime
        if not self.isValid():
            return None

        if "EXIF DateTimeOriginal" in self.tags:
            dateTimeString = self.tags["EXIF DateTimeOriginal"].values
            self._datetime = datetime.strptime(dateTimeString,
                '%Y:%m:%d %H:%M:%S')
        else:
            logging.warning("No DateTime information found in '{}'".format(
                self.picFileName))

        return self._datetime

    def coordinates(self):
        """
        Return a tuple representing the longitude and latidue of the gps
        coordinates of the picture location
        Kudos to https://github.com/laszukdawid
        for providing a nice example of how to extract decimal coordinates
        from exif coordinate ratios: https://github.com/ianare/exif-py/issues/66
        """

        if self._coordinates != (None, None):
            return self._coordinates
        if not self.isValid():
            return (None, None)

        lng_ref_tag_name = "GPS GPSLongitudeRef"
        lng_tag_name = "GPS GPSLongitude"
        lat_ref_tag_name = "GPS GPSLatitudeRef"
        lat_tag_name = "GPS GPSLatitude"

        # Check if these tags are present
        gps_tags = [lng_ref_tag_name,lng_tag_name,lat_tag_name,lat_tag_name]
        for tag in gps_tags:
            if not tag in self.tags.keys():
                logging.warning("Could not extract gps coordinates. "
                    "No '{0}' exif tag found in '{1}'".format(tag,
                        self.picFileName))
                return (None, None)

        convert = lambda ratio: float(ratio.num)/float(ratio.den)

        lng_ref_val = self.tags[lng_ref_tag_name].values
        lng_coord_val = [convert(c) for c in self.tags[lng_tag_name].values]

        lat_ref_val = self.tags[lat_ref_tag_name].values
        lat_coord_val = [convert(c) for c in self.tags[lat_tag_name].values]

        lng_coord = sum([c/60**i for i,c in enumerate(lng_coord_val)])
        lng_coord *= (-1)**(lng_ref_val=="W")

        lat_coord = sum([c/60**i for i,c in enumerate(lat_coord_val)])
        lat_coord *= (-1)**(lat_ref_val=="S")

        self._coordinates = (lng_coord, lat_coord)

        return self._coordinates

    def location(self):
        """
        Return a location object representing information about the location
        the picture was taken at
        """
        if self._location is not None:
            return self._location
        if not self.isValid():
            return None

        (lng, lat) = self.coordinates()
        if lng is not None and lat is not None:
            temp_loc = Location(lng,lat)
            if temp_loc.isValid():
                self._location = temp_loc
            else:
                logging.warning("'{0}' has an invalid location at coordinates "
                    "({1},{2})".format(self.picFileName, lng, lat))
        else:
            logging.warning("Could not extract coordinates from '{}'".format(
                self.picFileName))

        return self._location

