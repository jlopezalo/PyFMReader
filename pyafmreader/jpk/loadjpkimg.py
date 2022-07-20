import contextlib
import io
import numpy as np
import tifffile
from fasterzip import ZipFile

# As for 20/07/2022 these are the accepted channels for
# JPK files. This routine has a lot of hard coded values
# i.e: offset to search for the conversion factors, that are
# susceptible to breaking if the format is modified in any way.
valid_channels = [
    'Baseline', 'Height(measured)', 'SlopeFit', 'Adhesion', 'Height'
]

def get_channel_conversion_factors(tif_tags_list):
    """
    Get the conversion factors for each channel in the image.
    At the moment (last review 20/07/2022) these factors are stored
    in the tiff tags towards the end. To get this parameters the last
    6 tags are fetched and the information is extracted as follows:
    Example conversion factors:
    ['Calibrated height', 'SignedInteger', 'm', 'LinearScaling', -1.6953501835001456e-16, 6.218212395112357e-06]
    [name of the calibration, value type, units, scaling mode, multiplier, offset]
            
            Parameters:
                    tif_tags_list (list): list containing the page tags.
            
            Returns:
                    mult (float): multiplier to scale the raw data into the right units.
                    offset (float): offset to scale the raw data into the right units.
    """
    info = tif_tags_list[-6:]
    mult = info[-2]
    offset = info[-1]
    return mult, offset

def loadJPKimg(UFF):
    """
    Returns the contents of the data-image file inside the JPK file.
    This file is structured in a tiff like strucure, with each channel
    having its own page (slice) and tags (metadata).
    On the metadata the factors to scale the data into the right units
    can be found.
    The data is scaled as follows: raw_data * mult + offset
    
            Parameters:
                    UFF (uff.UFF): UFF object containing the JPK file metadata.
            
            Returns:
                    imagedata (dict): dictionary containing all the channels data.
    """
    file_type = UFF.filemetadata['file_type']
    if file_type == ".jpk-force-map": path = 'data-image.force'
    elif file_type == ".jpk-qi-data": path = 'data-image.jpk-qi-image'
    else: return
    with open(UFF.filemetadata['file_path'], 'rb') as file:
        afm_file = ZipFile(file)
        with afm_file.read(bytes(path, 'utf-8')) as filecontents:
            bytes_io = io.BytesIO(filecontents)
            with tifffile.TiffFile(bytes_io) as tif:
                data = {}
                for page in tif.pages[1:]:
                    tif_tags = [tag.value for tag in page.tags.values()]
                    for tag in tif_tags:
                        with contextlib.suppress(TypeError):
                            if 'algorithm.object-name.base-object-name.fancy-name' in tag:
                                channel_name = tag.split('\n')[0].split(':')[1].replace(' ', '')
                    if channel_name not in  valid_channels:
                        continue
                    # Try to fetch the multiplier and offset.
                    try:
                        mult, offset = get_channel_conversion_factors(tif_tags)
                    except IndexError:
                        mult, offset = 1.0, 0.0
                    # Check if the multiplier and the offset have been extracted properly.
                    # In the test files it works correctly. But weird things may happen with
                    # other files.
                    if isinstance(mult, float) and isinstance(offset, float):
                        image = page.asarray()
                        data[channel_name] = image.astype(np.int64) * mult + offset
    return data

def computeJPKPiezoImg(UFF):
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
                [UFF._loadcurve(idx, afm_file, file_type).extend_segments[0][1].segment_formated_data[height_channel_key][-1] for idx in range(UFF.filemetadata['Entry_tot_nb_curve'])]
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