# File containing the UFF class.
# Used to store data and metadata.

from fasterzip import ZipFile

from .constants import *
from .jpk.loadjpkcurve import loadJPKcurve
from .jpk.loadjpkimg import loadJPKimg
from .nanosc.loadnanosccurve import loadNANOSCcurve
from .nanosc.loadnanoscimg import loadNANOSCimg
from .load_uff import loadUFFcurve
from .save_uff import saveUFFtxt

class UFF:
    """
    Class used to store the data and metadata of an AFM file.

            Properties:
                    filemetadata (dict): Dictionary containing the file metadata.
                    isFV (bool): Flag indicating if the file is a Force Volume or not.
                    piezoimg (np.array): 2D np.array containing the piezo image of the file.
                    imagedata (dict): dictionary containing additional image data.
            
            Methods:
                    getcurve
                    getpiezoimg
                    to_txt

    """
    def __init__(self):
        self.filemetadata=None
        # JPK Specific Atributes
        self._sharedataprops=None
        self._groupedpaths=None
        # FV Specific Atribtues
        self.isFV=None
        self.piezoimg=None
        # In files like JPK scans you may
        # have additional image data.
        self.imagedata=None
    
    def _loadcurve(self, curveidx, afmfile, file_type):
        """
        Hidden function used to load a single curve from a file.
        
        Supported formats:
            - JPK --> .jpk-force, .jpk-force-map, .jpk-qi-data
            - NANOSCOPE --> .spm, .pfc
            - UFF --> .uff

                Parameters:
                        curveidx (int): Index of curve to load.
                        afmfile (ZipFile): Buffer containing the data of the AFM file. Only used for JPK files.
                        file_type (str): File extension.
                
                Returns:
                        FC (utils.forcecurve.ForceCurve): ForceCurve object containing the force curve data.
        """
        if file_type in jpkfiles:
            curvepaths = self._groupedpaths[curveidx]
            FC = loadJPKcurve(
                curvepaths, afmfile, curveidx, self.filemetadata
            )
        elif file_type in nanoscfiles:
            FC = loadNANOSCcurve(curveidx, self.filemetadata)
        elif file_type in ufffiles:
            FC = loadUFFcurve(self.filemetadata)
        return FC

    def getcurve(self, curveidx):
        """
        Function used to load a single curve from a file.
        
        Supported formats:
            - JPK --> .jpk-force, .jpk-force-map, .jpk-qi-data
            - NANOSCOPE --> .spm, .pfc
            - UFF --> .uff

                Parameters:
                        curveidx (int): Index of curve to load.
                
                Returns:
                        FC (utils.forcecurve.ForceCurve): ForceCurve object containing the force curve data.
        """
        file_type = self.filemetadata['file_type']
        if file_type in jpkfiles:
            with open(self.filemetadata['file_path'], 'rb') as file:
                afmfile = ZipFile(file)
                FC = self._loadcurve(curveidx, afmfile, file_type)
        elif file_type in nanoscfiles:
            FC = self._loadcurve(curveidx, None, file_type)
        elif file_type in ufffiles:
            FC = self._loadcurve(None, None, file_type)
        return FC
    
    def getpiezoimg(self):
        """
        Function used to compute the piezo image of a file.

        It is required that the file is a Force Volume.
        
        Supported formats:
            - JPK --> .jpk-force-map, .jpk-qi-data
            - NANOSCOPE --> .spm, .pfc

                Parameters: None
                
                Returns:
                        piezoimg (np.array): 2D array containing the piezo image of the file.
        """
        file_type = self.filemetadata['file_type']
        if file_type in jpkfiles:
            self.piezoimg = loadJPKimg(self)
        elif file_type in nanoscfiles:
            self.piezoimg = loadNANOSCimg(self.filemetadata)
        return self.piezoimg
    
    def to_txt(self, savedir):
        """
        Function used to save the loaded data into a txt file following the UFF.

                Parameters:
                        savedir (str): Path to save the txt UFF file.
                
                Returns: None
        """
        if self.isFV:
            for curveidx in range(self.filemetadata['Entry_tot_nb_curve']):
                saveUFFtxt(self, self, savedir, curveidx)
        else:
            saveUFFtxt(self, self, savedir)
        
