from struct import unpack
from itertools import groupby
import numpy as np

from jpk.parsejpkheader import parseJPKsegmentheader
from importutils import ForceCurve, Segment

def loadJPKcurve(paths, afm_file, curve_index, file_metadata, shared_data_properties):

    file_id = file_metadata['file_id']
    curve_properties = file_metadata['curve_properties']

    force_curve = ForceCurve(curve_index, file_id)

    index = 1 if file_metadata["real_num_pixels"] == 0 else 3

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

        segment = Segment(file_id, segment_id, segment_type)
        segment.segment_formated_data = segment_formated_data
        segment.segment_raw_data = segment_raw_data
        segment.segment_metadata = curve_properties[str(curve_index)][segment_id]

        if segment.segment_type == "extend":
            force_curve.extend_segments.append((segment.segment_id, segment))
        elif segment.segment_type == "retract":
            force_curve.retract_segments.append((segment.segment_id, segment))
        elif segment.segment_type == "pause":
            force_curve.pause_segments.append((segment.segment_id, segment))
        elif segment.segment_type == "modulation":
            force_curve.modulation_segments.append((segment.segment_id, segment))

    return force_curve