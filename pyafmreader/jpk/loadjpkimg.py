import numpy as np
from fasterzip import ZipFile

def loadJPKimg(UFF):
    """
    Function used to compute the piezo image of a JPK file.

            Parameters:
                    UFF (uff.UFF): UFF object containing the JPK file metadata.
            
            Returns:
                    piezoimg (np.array): 2D array containing the piezo image of the JPK file.
    """
    file_type = UFF.filemetadata['file_type']
    height_channel_key = UFF.filemetadata["height_channel_key"]
    if file_type in (".jpk-force-map", ".jpk-qi-data"):
        # Get height key
        # Get the last value of the first approach segment.
        with open(UFF.filemetadata['file_path'], 'rb') as file:
            afm_file = ZipFile(file)
            tempiezoimg = np.array(
                [UFF._loadcurve(idx, afm_file, file_type).extend_segments[0][1].segment_formated_data[height_channel_key][-1] for idx in range(UFF.filemetadata['real_num_pixels']+1)]
            )
        # Rescale piezo image (0 - maxval)
        piezoimg = tempiezoimg - np.min(tempiezoimg)
        # Reshape piezo image
        piezoimg = piezoimg.reshape((UFF.filemetadata["num_x_pixels"], UFF.filemetadata["num_y_pixels"]))
        if file_type == ".jpk-force-map":
            # Flip odd rows to follow raster scan direction properly.
            #   0  1  2       0  1  2
            #   3  4  5  -->  5  4  3
            #   6  7  8       6  7  8 
            piezoimg = np.asarray([row[::(-1)**i] for i, row in enumerate(piezoimg)])
        else:
            # In QI files it is not recessary to flip rows
            # due to how the acquisition mode works.
            piezoimg = piezoimg
    
    return piezoimg