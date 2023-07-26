# File containing the function loadNANOSCfile, 
# used to load the metadata of NANOSCOPE files.

from .parsenanoscheader import parseNANOSCheader

def loadNANOSCfile(filepath, UFF):
    """
    Function used to load the metadata of a NANOSCOPE file.

            Parameters:
                    filepath (str): File path to the NANOSCOPE file.
                    UFF (uff.UFF): UFF object to load the metadata into.
            
            Returns:
                    UFF (uff.UFF): UFF object containing the loaded metadata.
    """
    UFF.filemetadata = parseNANOSCheader(filepath)
    UFF.isFV = bool(UFF.filemetadata['force_volume'])
    return UFF
