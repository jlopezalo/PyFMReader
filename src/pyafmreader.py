import os
from constants import *
from jpk.loadjpkfile import loadJPKfile
from nanosc.loadnanoscfile import loadNANOSCfile
from uff import UFF

def loadfile(filepath):
    filesuffix = os.path.splitext(filepath)[-1]

    uffobj = UFF()

    if filesuffix in jpkfiles:
        uffobj = loadJPKfile(filepath, uffobj, filesuffix)
    
    elif filesuffix in nanoscfiles:
        uffobj = loadNANOSCfile(filepath, uffobj)
    
    return uffobj