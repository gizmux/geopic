import logging

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