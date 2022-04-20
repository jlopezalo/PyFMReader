
import os
import re
from constants import *

def parseJPKheader(filepath, header_properties, shared_data_properties):

    file_metadata = {}

    file_metadata["file_path"] = filepath
    file_metadata["file_name"] = os.path.basename(filepath)
    file_metadata["file_size_bytes"] = os.path.getsize(filepath)
    file_metadata["file_type"] = os.path.splitext(filepath)[-1]
 
    file_id = re.search(r'(\d{2}.\d{2}.\d{2}.\d{3})', filepath)
    if file_id:
        file_metadata["file_id"] = file_id.group(1)
    else:
        # If the file has been renamed, then assign the file id to be the file name.
        file_metadata["file_id"] = file_metadata["file_name"]

    if file_metadata["file_type"] == ".jpk-force-map":
        prefix = "force-scan-map"
        pre_header = ".settings"
    elif file_metadata["file_type"] == ".jpk-qi-data":
        prefix = "quantitative-imaging-map"
        pre_header = ".settings"
    elif file_metadata["file_type"] == ".jpk-force":
        prefix = "force-scan-series"
        pre_header = ".header"
    
    file_metadata["Experimental_instrument"] = header_properties.get(prefix + ".description.instrument")
    file_metadata["JPK_file_format_version"] = header_properties.get("file-format-version")
    file_metadata["JPK_software_version"] = header_properties.get(prefix + ".description.source-software")
    file_metadata["retracted_delay"] = float(header_properties.get(prefix + ".settings.force-settings.retracted-pause-time", default_delay))
    file_metadata["extended_delay"] = float(header_properties.get(prefix + ".settings.force-settings.extended-pause-time", default_delay))
    file_metadata["file_date"] = header_properties.get(prefix + ".start-time")
    
    file_metadata["scan_angle"] = float(header_properties.get(prefix + ".position-pattern.grid.theta", default_angle))

    file_metadata["num_x_pixels"] = int(header_properties.get(prefix + ".position-pattern.grid.ilength", multiplier_default))
    file_metadata["num_y_pixels"] = int(header_properties.get(prefix + ".position-pattern.grid.jlength", multiplier_default))

    file_metadata["scan_size_x"] = float(header_properties.get(prefix + ".position-pattern.grid.ulength", offset_default)) * scaling_factor
    file_metadata["scan_size_y"] = float(header_properties.get(prefix + ".position-pattern.grid.vlength", offset_default)) * scaling_factor
    
    file_metadata["z_closed_loop_status"] = header_properties.get(prefix + ".settings.force-settings.closed-loop", boolean_default)
    if file_metadata["z_closed_loop_status"] == "true": file_metadata["z_closed_loop_status"] = "On"
    elif file_metadata["z_closed_loop_status"] == "false": file_metadata["z_closed_loop_status"] = "Off"

    file_metadata["real_num_pixels"] = int(header_properties.get(prefix + ".indexes.max", offset_default))
    file_metadata["extend_pause_duration"] = float(header_properties.get(prefix + ".settings.force-settings.extended-pause-time", offset_default))

    if file_metadata["file_type"] in (".jpk-force"):
        file_metadata["relative_z_start"] = float(header_properties.get("relative-z-start", offset_default)) * scaling_factor
        file_metadata["relative_z_end"] = float(header_properties.get("relative-z-end", offset_default)) * scaling_factor
        file_metadata["relative_ramp_size"] = file_metadata["relative_z_end"] - file_metadata["relative_z_start"] # This can be 0
    
    elif file_metadata["file_type"] in (".jpk-qi-data"):
        file_metadata["relative_z_start"] = float(header_properties.get("settings.force-settings.extend.z-start", offset_default)) * scaling_factor
        file_metadata["relative_z_end"] = float(header_properties.get("settings.force-settings.extend.z-end", offset_default)) * scaling_factor
        file_metadata["relative_ramp_size"] = file_metadata["relative_z_end"] - file_metadata["relative_z_start"] # This can be 0
    
    file_metadata["force_setpoint"] = float(header_properties.get(prefix + pre_header + ".force-settings.relative-setpoint", offset_default))

    # Get number of channels saved
    file_metadata["nbr_channels"] = int(shared_data_properties["lcd-infos.count"])

    # Get channel properties
    channel_properties = {}
    for channel_id in range(file_metadata["nbr_channels"]):
        
        properties = {}
        properties["channel_id"] = channel_id
        
        pre = f"lcd-info.{channel_id}"
        pre_conv = pre + ".conversion-set"
        conv_distance = ".conversion.distance"
        conv_force = ".conversion.force"
        conv_absolute = ".conversion.absolute"
        conv_nominal = ".conversion.nominal"

        channel_name = shared_data_properties.get(pre + ".channel.name")

        if channel_name in ("vDeflection", "hDeflection"):
            properties["encoder_offet_key"] = float(shared_data_properties.get(pre + ".encoder.scaling.offset", offset_default))
            properties["encoder_multiplier_key"] = float(shared_data_properties.get(pre + ".encoder.scaling.multiplier", multiplier_default))

            properties["base"] = shared_data_properties.get(pre_conv + ".conversions.base")
            
            properties["base_defined"] = shared_data_properties.get(pre_conv + ".conversion." + properties["base"] + ".defined", boolean_default)
            if properties["base_defined"] == "true": 
                properties["base_defined"] = True
                print(f'[!] The conversion base for {properties["base"]} has been already been defined. Check your loaded data.')
            elif properties["base_defined"] == "false": 
                properties["base_defined"] = False
                
            properties["distance_defined"] = shared_data_properties.get(pre_conv + conv_distance + ".defined", boolean_default)
            if properties["distance_defined"] == "true":
                properties["distance_defined"] = True
            elif properties["distance_defined"] == "false": 
                properties["distance_defined"]= False
            properties["deflection_distance_offset"] = float(shared_data_properties.get(pre_conv + conv_distance + ".scaling.offset", offset_default)) * scaling_factor # in nm/V
            properties["deflection_distance_multiplier"] = float(shared_data_properties.get(pre_conv + conv_distance + ".scaling.multiplier", offset_default)) * scaling_factor # in nm/V

            properties["force_defined"] = shared_data_properties.get(pre_conv + conv_force + ".defined", boolean_default)
            if properties["force_defined"] == "true":
                properties["force_defined"] = True
            elif properties["force_defined"] == "false": 
                properties["force_defined"] = False
            properties["deflection_force_offset"] = float(shared_data_properties.get(pre_conv + conv_force + ".scaling.offset", offset_default))
            properties["deflection_force_multiplier"] = float(shared_data_properties.get(pre_conv + conv_force + ".scaling.multiplier", multiplier_default))

            if channel_name == "vDeflection":
                file_metadata["original_deflection_sensitivity"] = float(properties.get("deflection_distance_multiplier", multiplier_default))
                file_metadata["original_spring_constant"] = float(properties.get("deflection_force_multiplier", multiplier_default))

                if not properties["distance_defined"] and not properties["force_defined"]:
                    print(f"[!] In the file's {file_metadata['file_id']} header the deflection sensitivity and spring constant could not be found,\
                             the default values of dlection sentivity = {multiplier_default} and K = {multiplier_default} have been assigned!")

        
        elif channel_name in ("capacitiveSensorHeight", "measuredHeight", "height"):
            properties["encoder_offet_key"] = float(shared_data_properties.get(pre + ".encoder.scaling.offset", offset_default))
            properties["encoder_multiplier_key"] = float(shared_data_properties.get(pre + ".encoder.scaling.multiplier", scaling_factor))
            
            properties["base"] = shared_data_properties.get(pre_conv + ".conversions.base")

            properties["base_defined"] = shared_data_properties.get(pre_conv + ".conversion." + properties["base"] + ".defined", boolean_default)
            if properties["base_defined"] == "true":
                properties["base_defined"] = True
                print(f'[!] The conversion base for {properties["base"]} has been already been defined. Check your loaded data.')
            elif properties["base_defined"] == "false": 
                properties["base_defined"] = False

            properties["absolute_defined"] = shared_data_properties.get(pre_conv + conv_absolute + ".defined", boolean_default)
            if properties["absolute_defined"] == "true":
                properties["absolute_defined"] = True
            elif properties["absolute_defined"] == "false": 
                properties["absolute_defined"] = False
            properties["capSensHeight_abs_offset"] = float(shared_data_properties.get(pre_conv + conv_absolute + ".scaling.offset", offset_default))
            properties["capSensHeight_abs_mult"] = float(shared_data_properties.get(pre_conv + conv_absolute + ".scaling.multiplier", scaling_factor))

            properties["nominal_defined"] = shared_data_properties.get(pre_conv + conv_nominal + ".defined", boolean_default)
            if properties["nominal_defined"] == "true":
                properties["nominal_defined"] = True
            elif properties["nominal_defined"] == "false": 
                properties["nominal_defined"] = False
            properties["capSensHeight_nom_offset"] = float(shared_data_properties.get(pre_conv + conv_nominal + ".scaling.offset", offset_default))
            properties["capSensHeight_nom_mult"] = float(shared_data_properties.get(pre_conv + conv_nominal + ".scaling.multiplier", scaling_factor))
        
        channel_properties[channel_name] = properties
    
    file_metadata["channel_properties"] = channel_properties
    
    # Get number of segments saved
    if file_metadata["file_type"] == ".jpk-force":
        file_metadata["nbr_segments"] = int(header_properties.get(f"force-scan-series.force-segments.count", num_segments_default))
    else:
        file_metadata["nbr_segments"] = int(shared_data_properties.get(f"force-segment-header-infos.count", num_segments_default))

    # Create empty key for holding segment properties
    file_metadata["curve_properties"] = {}
    
    return file_metadata

def parseJPKsegmentheader(curve_properties, curve_index, file_type, segment_header, shared_data_properties, segment_id):
    
    segment_metadata = {}

    # Parameters always found in the segment header
    segment_metadata["time_stamp"] = segment_header.get("force-segment-header.time-stamp")
    segment_metadata["num_points"] = int(segment_header.get("force-segment-header.num-points"))
    segment_metadata["duration"] = float(segment_header.get("force-segment-header.duration"))
    segment_metadata["channels"] = segment_header.get("channels.list").split(" ")

    segment_metadata["baseline_measured"] = segment_header.get("force-segment-header.baseline.measured", boolean_default)
    if segment_metadata["baseline_measured"] == "true":
        segment_metadata["baseline_measured"] = True
    elif segment_metadata["baseline_measured"] == "false":
        segment_metadata["baseline_measured"] = False
    segment_metadata["baseline"] = float(segment_header.get("force-segment-header.baseline.baseline", offset_default))

    if file_type == ".jpk-force":
        segment_metadata["approach_id"] = segment_header.get("force-segment-header.approach-id")
        segment_metadata["style"] = segment_header.get("force-segment-header.settings.style")

        if segment_metadata["style"] == "extend":
            segment_metadata["setpoint"] = float(segment_header.get("force-segment-header.settings.segment-settings.setpoint", multiplier_default))
        
        elif segment_metadata["style"] == "modulation":
            segment_metadata["amplitude"] = float(segment_header.get("force-segment-header.settings.segment-settings.amplitude", offset_default))
            segment_metadata["frequency"] = float(segment_header.get("force-segment-header.settings.segment-settings.frequency", offset_default))
            segment_metadata["start-phase"] = float(segment_header.get("force-segment-header.settings.segment-settings.start-phase", offset_default))
        
        segment_metadata["z_start"] = float(segment_header.get("force-segment-header.settings.segment-settings.z-start", offset_default)) * scaling_factor
        segment_metadata["z_end"] = float(segment_header.get("force-segment-header.settings.segment-settings.z-end", offset_default)) * scaling_factor
    
    elif file_type in (".jpk-force-map", ".jpk-qi-data"):
        prefix = f"force-segment-header-info.{segment_id}"
        segment_metadata["approach_id"] = shared_data_properties.get(f"{prefix}.approach-id")
        segment_metadata["style"] = shared_data_properties.get(f"{prefix}.settings.style")

        if segment_metadata["style"] == "extend":
            segment_metadata["setpoint"] = float(shared_data_properties.get(f"{prefix}.settings.segment-settings.setpoint", multiplier_default))

        elif segment_metadata["style"] == "modulation":
            segment_metadata["amplitude"] = float(shared_data_properties.get(f"{prefix}.settings.segment-settings.amplitude", offset_default))
            segment_metadata["frequency"] = float(shared_data_properties.get(f"{prefix}.settings.segment-settings.frequency", offset_default))
            segment_metadata["start-phase"] = float(shared_data_properties.get(f"{prefix}.settings.segment-settings.start-phase", offset_default))
        
        segment_metadata["z_start"] = float(shared_data_properties.get(f"{prefix}.settings.segment-settings.z-start", offset_default)) * scaling_factor
        segment_metadata["z_end"] = float(shared_data_properties.get(f"{prefix}.settings.segment-settings.z-end", offset_default)) * scaling_factor
    
    # Compute ramp size
    segment_metadata["ramp_size"] = segment_metadata["z_end"] - segment_metadata["z_start"]
    # Compute ramp speed
    segment_metadata["ramp_speed"] = segment_metadata["ramp_size"] / segment_metadata["duration"]

    curve_properties[str(curve_index)].update({segment_id: segment_metadata})
    
    return curve_properties