
from .parsenanoscheader import parseNANOSCheader

def loadNANOSCfile(filepath, UFF):
    UFF.filemetadata = parseNANOSCheader(filepath)
    UFF.isFV = bool(UFF.filemetadata['force_volume'])
    return UFF
