
from nanosc.parsenanoscheader import parseNANOSCheader

def loadNANOSCfile(filepath, UFF):
    UFF.filemetadata = parseNANOSCheader(filepath)
    return UFF




