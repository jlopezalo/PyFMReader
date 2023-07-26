# File containing the function loadfile,
# used as an entry point to load different
# AFM data format files.

import os
from .constants import *
from .jpk.loadjpkfile import loadJPKfile
from .jpk.loadjpkthermalfile import loadJPKThermalFile
from .nanosc.loadnanoscfile import loadNANOSCfile
from .load_uff import loadUFFtxt
from .uff import UFF

def loadfile(filepath):
    """
    Load AFM file. 
    
    Supported formats:
        - JPK --> .jpk-force, .jpk-force-map, .jpk-qi-data
        - JPK Thermal --> .tnd
        - NANOSCOPE --> .spm, .pfc, .00X
        - UFF --> .uff

            Parameters:
                    filepath (str): Path to the file.
            
            Returns:
                    If JPK, NANOSCOPE OR UFF:
                        UFF (uff.UFF): Universal File Format object containing loaded data.
                    If JPK Thermal:
                        Amplitude (m^2/V) (np.array),
                        Frequencies (Hz) (np.array),
                        Fit-Data (m^2/V) (np.array),
                        Parameters (dict)


    """
    split_path = filepath.split(os.extsep)
    # Depending on the configuration of the OS, JPK files have the following
    # extension: .jpk-force.zip
    if split_path[-1] == 'zip': filesuffix = split_path[-2]
    else: filesuffix = split_path[-1]

    uffobj = UFF()

    if filesuffix[1:].isdigit() or filesuffix in nanoscfiles:
        return loadNANOSCfile(filepath, uffobj)

    elif filesuffix in jpkfiles:
        return loadJPKfile(filepath, uffobj, filesuffix)
    
    elif filesuffix in ufffiles:
        return loadUFFtxt(filepath, uffobj)
    
    elif filesuffix in jpkthermalfiles:
        return loadJPKThermalFile(filepath)
    else:
        Exception(f"Can not load file: {filepath}")