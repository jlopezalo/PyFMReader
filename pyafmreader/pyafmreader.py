# File containing the function loadfile,
# used as an entry point to load different
# AFM data format files.

import os
from .constants import *
from .jpk.loadjpkfile import loadJPKfile
from .nanosc.loadnanoscfile import loadNANOSCfile
from .load_uff import loadUFFtxt
from .uff import UFF

def loadfile(filepath):
    """
    Load AFM file. Supported formats:
    - JPK --> '.jpk-force', '.jpk-force-map', '.jpk-qi-data'

            Parameters:
                    uffpath (str): Path to the file.
            
            Returns:
                    header (dict): Dictionary containing the header information.
    """
    filesuffix = os.path.splitext(filepath)[-1]

    uffobj = UFF()

    if filesuffix in jpkfiles:
        uffobj = loadJPKfile(filepath, uffobj, filesuffix)
    
    elif filesuffix in nanoscfiles:
        uffobj = loadNANOSCfile(filepath, uffobj)
    
    elif filesuffix in ufffiles:
        uffobj = loadUFFtxt(filepath, uffobj)
    
    return uffobj