# File containing the loadJPKcurve function,
# used to load single force curves from JPK files.

from struct import unpack
from itertools import groupby
import numpy as np

from ..utils.forcecurve import ForceCurve
from ..utils.segment import Segment
from ..constants import JPK_SETPOINT_MODE

def loadJPKcurve(paths, afm_file, curve_index, file_metadata):
    """
    Function used to load the data of a single force curve from a JPK file.

            Parameters:
                    paths (list): list containing the paths of the files present int the JPK file.
                    afm_file (ZipFile): ZipFile buffer containing the data of the JPK file.
                    curve_index (int): Index of curve to load.
                    file_metadata (dict): Dictionary containing the file metadata.
            
            Returns:
                    force_curve (utils.forcecurve.ForceCurve): ForceCurve object containing the loaded data.
    """
    file_id = file_metadata['file_id']
    curve_properties = file_metadata['curve_properties']

    force_curve = ForceCurve(curve_index, file_id)

    curve_indices = file_metadata["Entry_tot_nb_curve"] - 1

    index = 1 if curve_indices == 0 else 3

    keyf = lambda text: text.split("/")[index]
    groupded_paths = [list(items) for _, items in groupby(sorted(paths), key=keyf)][1:]

    for segment_group in groupded_paths:
        segment_id = segment_group[0].split("/")[index]
        segment_raw_data = {}
        segment_formated_data = {}

        for path in segment_group:
            data_type = path.split("/")[-1].split(".")[0]

            if data_type not in ['', 'segment-header']:
                nbr_points = afm_file.getinfo(bytes(path, 'utf-8')).get('m_uncomp_size') // 4
                with afm_file.read(bytes(path, 'utf-8')) as filecontents:
                    data_raw = unpack(f">{str(nbr_points)}i", filecontents)
                    segment_raw_data[data_type] = data_raw
        
        height_channel_key = file_metadata['height_channel_key']
        found_vDeflection = file_metadata['found_vDeflection']

        # Transform Height data
        if height_channel_key is not None:
            raw_data = segment_raw_data[height_channel_key]
            raw_data = np.asarray(raw_data)
            conversion_factors = file_metadata["channel_properties"][height_channel_key]
            values = raw_data * conversion_factors["encoder_multiplier_key"] + conversion_factors["encoder_offet_key"]

            if conversion_factors["absolute_defined"]:
                values = values * conversion_factors["capSensHeight_abs_mult"] +  conversion_factors["capSensHeight_abs_offset"]

            if conversion_factors["nominal_defined"]:
                values = values * conversion_factors["capSensHeight_nom_mult"] +  conversion_factors["capSensHeight_nom_offset"]

            segment_formated_data[height_channel_key] = values

        else:
            print("[!] No valid height channel found!")

        # Transform vDeflection data
        if found_vDeflection:
            raw_data = segment_raw_data["vDeflection"]
            raw_data = np.asarray(raw_data)
            conversion_factors = file_metadata["channel_properties"]["vDeflection"]
            segment_formated_data["vDeflection"] = raw_data * \
                conversion_factors["encoder_multiplier_key"] + \
                conversion_factors["encoder_offet_key"] + \
                conversion_factors["deflection_distance_offset"]

        else:
            print("[!] No valid vDeflection channel found!")
        segment_type = curve_properties[str(curve_index)][segment_id]["style"]
        segment_duration = curve_properties[str(curve_index)][segment_id]["duration"]
        segment_num_points = curve_properties[str(curve_index)][segment_id]["num_points"]

        # TO DO: Time can be exported, handle this situation.
        segment_formated_data["time"] = np.linspace(0, segment_duration, segment_num_points, endpoint=False)

        if segment_type=='extend': segment_type='Approach'
        elif segment_type == 'pause': segment_type = 'Pause'
        elif segment_type == 'modulation': segment_type = 'Modulation'
        elif segment_type=='retract': segment_type='Retract'

        segment = Segment(file_id, segment_id, segment_type)
        segment.segment_formated_data = segment_formated_data
        segment.segment_raw_data = segment_raw_data
        segment.segment_metadata = curve_properties[str(curve_index)][segment_id]
        segment.force_setpoint_mode = JPK_SETPOINT_MODE
        segment.nb_point = segment_num_points
        segment.nb_col = len(segment_formated_data.keys())
        segment.force_setpoint = file_metadata["force_setpoint"]
        segment.velocity = segment.segment_metadata["ramp_speed"]
        segment.sampling_rate = segment.nb_point / segment.segment_metadata["duration"]
        segment.z_displacement = segment.segment_metadata["ramp_size"]


        if segment.segment_type == "Approach":
            force_curve.extend_segments.append((int(segment.segment_id), segment))
        elif segment.segment_type == "Retract":
            force_curve.retract_segments.append((int(segment.segment_id), segment))
        elif segment.segment_type == "Pause":
            force_curve.pause_segments.append((int(segment.segment_id), segment))
        elif segment.segment_type == "Modulation":
            force_curve.modulation_segments.append((int(segment.segment_id), segment))

    return force_curve