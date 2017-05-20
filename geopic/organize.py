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
            fileNamePath = dirname+file
            if imghdr.what(fileNamePath) == 'jpeg':
                print fileNamePath

    def __init__(self, picFolderPath):
        self.picFolderPath  = picFolderPath
        self.valid          = False
        self._picinfo       = None

        try:
            path.walk(picFolderPath, Organize._visitPath, self)
        except IOError as e:
            logging.error("Unable to organize '{0}' because '{1}'".format(
                picFolderPath, e))
            #TODO: CONSIDER: is this the best strategy here ?
            return

        if self._picinfo is not None:
            self.valid = True

    def isValid(self):
        return self.valid




