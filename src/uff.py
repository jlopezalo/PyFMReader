from math import nan
import zipfile
import numpy as np

from fasterzip import ZipFile

from constants import *
from jpk.loadjpkcurve import loadJPKcurve
from jpk.loadjpkimg import loadJPKimg
from nanosc.loadnanosccurve import loadNANOSCcurve
from nanosc.loadnanoscimg import loadNANOSCimg

class UFF:
    def __init__(self):
        self.filemetadata=None
        # JPK Specific Atributes
        self._sharedataprops=None
        self._groupedpaths=None
        # FV Specific Atribtues
        self.isFV=None
        self.piezoimg=None
        self.qualitymap=None
    
    def _loadcurve(self, curveidx, afmfile, file_type):
        if file_type in jpkfiles:
            curvepaths = self._groupedpaths[curveidx]
            FC = loadJPKcurve(
                curvepaths, afmfile, curveidx, self.filemetadata, self._sharedataprops
            )
        elif file_type in nanoscfiles:
            FC = loadNANOSCcurve(curveidx, self.filemetadata)
        return FC

    def getcurve(self, curveidx):
        file_type = self.filemetadata['file_type']
        if file_type in jpkfiles:
            with open(self.filemetadata['file_path'], 'rb') as file:
                afmfile = ZipFile(file)
                FC = self._loadcurve(curveidx, afmfile, file_type)
        elif file_type in nanoscfiles:
            FC = self._loadcurve(curveidx, None, file_type)
        return FC
    
    def getpiezoimg(self):
        file_type = self.filemetadata['file_type']
        if file_type in jpkfiles:
            return loadJPKimg(self)
        elif file_type in nanoscfiles:
            return loadNANOSCimg(self.filemetadata)

