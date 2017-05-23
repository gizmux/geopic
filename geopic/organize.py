import logging
import imghdr
from os import path

from .picinfo import PicInfo

class Organize:
    """
    Organize a set of pictures in specified subgroups
    based on picture information
    """

    def _visitPath(self, dirname, filenames):
        for file in filenames:
            filenameWithPath = path.join(dirname, file)
            if path.isfile(filenameWithPath) and (
                imghdr.what(filenameWithPath) == 'jpeg'):
                # found a jpeg file. Lets add it to our internal
                # picinfo structure
                if filenameWithPath not in self._picinfo:
                    self._picinfo[filenameWithPath] = PicInfo(filenameWithPath)
                else:
                    logging.warning(
                        "Found '{0}' more than once while traversing '{1}'".
                        format(filenameWithPath, dirname))

    def __init__(self, picFolderPath):
        self.picFolderPath  = picFolderPath
        self.valid          = False
        self._picinfo       = dict()

        try:
            path.walk(picFolderPath, Organize._visitPath, self)
        except IOError as e:
            logging.error("Unable to organize '{0}' because '{1}'".format(
                picFolderPath, e))
            #TODO: CONSIDER: is this the best strategy here ?
            return

        if len(self._picinfo) > 0:
            self.valid = True

    def isValid(self):
        return self.valid




