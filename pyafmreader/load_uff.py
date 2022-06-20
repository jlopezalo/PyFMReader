# File containing the functions used to load AFM data
# saved using the Universal File Format described in:
# Reference: N/A

import os
from .utils.forcecurve import ForceCurve
from .utils.segment import Segment
import numpy as np

def loadUFFheader(uffpath):
    """
    Load the header of an UFF AFM file.

            Parameters:
                    uffpath (str): Path to the file.
            
            Returns:
                    header (dict): Dictionary containing the header information.
    """
    header = {
        'file_path': uffpath,
        "file_size_bytes": os.path.getsize(uffpath)
    }
    header["file_type"] = os.path.splitext(uffpath)[-1]
    with open(uffpath, 'r') as file:
        for line in file.readlines():
            if 'HE' in line:
                splitline = line.split(' ', 1)[-1].split(':', 1)
                field = splitline[0]
                val = splitline[-1].lstrip().strip(' \n"')
                try: val = float(val)
                except ValueError: val = val
                header[field] = val
    return header

def loadUFFcurve(header):
    """
    Load the data of an UFF AFM file.

            Parameters:
                    header (dict): Dictionary containing the UFF header information.
            
            Returns:
                    fdc (utils.forcecurve.ForceCurve): Force Distance Curve data stored in UFF.
    """
    uffpath = header['file_path']
    idx = int(header['Recording_curve_id'])
    filename = header['Entry_filename']
    fdc = ForceCurve(idx, filename)
    for segid in range(int(header['Recording_number_segment'])):
        segtype = header[f'Recording_segment_{segid}_type']
        segcode = header[f'Recording_segment_{segid}_code']
        npoints = int(header[f'Recording_segment_{segid}_nb_point'])
        ncols = int(header[f'Recording_segment_{segid}_nb_col'])

        segdata = np.zeros((npoints, ncols))
        segment = Segment(filename, str(segid), segtype)
        segment.nb_point = npoints
        segment.nb_col = ncols
        segment.force_setpoint_mode = header[f'Recording_segment_{segid}_force_setpoint_mode']
        segment.force_setpoint = header[f'Recording_segment_{segid}_force_setpoint(N)']
        segment.velocity = header[f'Recording_segment_{segid}_velocity(m/s)']
        segment.sampling_rate = header[f'Recording_segment_{segid}_sampling_rate(Hz)']
        segment.z_displacement = header[f'Recording_segment_{segid}_z_displacement(m)']

        with open(uffpath, 'r') as file:
            i = 0
            for line in file.readlines():
                linedata = line.split()
                if linedata[0] != segcode: continue
                for j, value in enumerate(linedata[2:]): segdata[i,j] = value
                i+=1
        for colidx in range(ncols):
            colkey = header[f'Recording_segment_{segid}_col_{colidx}_title']
            if segment.segment_formated_data is None:
                segment.segment_formated_data = {colkey:segdata[:, colidx]}
            else:
                segment.segment_formated_data.update({colkey:segdata[:, colidx]})
        if segtype == 'Approach': fdc.extend_segments.append((segid, segment))
        elif segtype == 'Retract': fdc.retract_segments.append((segid, segment))
        elif segtype == 'Pause': fdc.pause_segments.append((segid, segment))
        elif segtype == 'Modulation': fdc.modulation_segments.append((segid, segment))
    return fdc

def loadUFFtxt(uffpath, UFF):
    """
    Load the data of a txt UFF AFM file.

            Parameters:
                    uffpath (str): Path to the file.
                    UFF (uff.UFF): Universal File Format object to store loaded data.
            
            Returns:
                    UFF (uff.UFF): Universal File Format object containing loaded data.
    """
    UFF.filemetadata = loadUFFheader(uffpath)
    return UFF