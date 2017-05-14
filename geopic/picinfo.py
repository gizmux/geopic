import logging
from datetime import datetime

import exifread

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