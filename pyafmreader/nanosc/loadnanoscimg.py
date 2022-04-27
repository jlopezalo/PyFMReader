# File containing the function loadNANOSCimg,
# used to load the piezo image from NANOSCOPE files.

import itertools
from struct import unpack
import numpy as np

def loadNANOSCimg(header):
    """
    Function used to load the piezo image from a NANOSCOPE file.

            Parameters:
                    header (dict): Dictionary containing the file metadata.
            
            Returns:
                    piezoimg (np.array): 2D array containing the piezo image.
    """
    filepath = header['file_path']
    with open(filepath, 'rb') as afmfile:
        fvimgoffset = header['FV_ima_offset']
        shape = [header['FV_nb_sampsline'], header['FV_nb_lines'], 1]
        temppiezoimg = np.zeros(shape, np.float)
        skip = ((header['FV_nb_sampsline'] / header['FDC_nb_sampsline']) - 1) * 2
        if fvimgoffset != 0:
            afmfile.seek(fvimgoffset, 0)
            image_bytes = header['FV_data_length'] // (header['FV_nb_sampsline'] * header['FV_nb_lines'])
            if image_bytes == 2: fmt = '<h' # short int
            elif image_bytes == 4: fmt = '<i' # int
            mult = header['FV_Zsens'] * header['zscan_sens_nmbyV'] / (2. ** (header['byte_per_pixel'] * 8))

            for i, j in itertools.product(range(header['FV_nb_lines']), range(header['FV_nb_sampsline'])):
                data = unpack(fmt, afmfile.read(image_bytes))
                temppiezoimg[i, j] = data[0] * mult
                if skip!=0:
                    afmfile.seek(skip, 1)

        return temppiezoimg - temppiezoimg.min()