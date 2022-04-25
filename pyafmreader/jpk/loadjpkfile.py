import os
from itertools import groupby
from fasterzip import ZipFile
from pyafmreader.jpk.parsejpkheader import parseJPKheader, parseJPKsegmentheader

def loadJPKfile(filepath, UFF, filesuffix):
    with open(filepath, 'rb') as file:
        afm_file =  ZipFile(file)

        # Get global metadata stored in the files: header.properties and shared-data/header.properties
        with afm_file.read(b'header.properties') as headercontents:
            header_properties_raw = bytes(headercontents).decode().splitlines()
            header_properties = {item.split("=")[0]:item.split("=")[1] for item in header_properties_raw if not item.startswith("#")}
        
        with afm_file.read(b'shared-data/header.properties') as sharedheadercontents:
            shared_data_properties_raw = bytes(sharedheadercontents).decode().splitlines()
            UFF._sharedataprops = {item.split("=")[0]:item.split("=")[1] for item in shared_data_properties_raw if not item.startswith("#")}

        UFF.filemetadata = parseJPKheader(filepath, header_properties, UFF._sharedataprops)

        paths = [name.decode() for name in afm_file.namelist() if "segments" in name.decode()]

        if filesuffix in (".jpk-force-map", ".jpk-qi-data"):
            # Function to group paths by index
            group_keyf = lambda text: int(text.split("/")[1])
            # Function to sort lists of paths by the index
            list_keyf = lambda list: int(list[0].split("/")[1])
            # Group all the paths of the same index
            grouped_paths = [list(items) for _, items in groupby(paths, key=group_keyf)]
            # Sort the path groups based on index
            grouped_paths = sorted(grouped_paths, key=list_keyf)

        else:
            # If not a map, all paths correspond to the same curve.
            grouped_paths = [paths]
        
        UFF._groupedpaths = grouped_paths

        curve_properties = {}

        index = 1 if UFF.filemetadata["Entry_tot_nb_curve"] == 0 else 3

        keyf = lambda text: text.split("/")[index]
        groupded_paths = [list(items) for _, items in groupby(sorted(paths), key=keyf)][1:]

        for segment_group in groupded_paths:
            if index == 3:
                curve_id = segment_group[0].split("/")[1]
            else:
                curve_id = '0'
            segment_id = segment_group[0].split("/")[index]
            if not curve_id in curve_properties.keys():
                curve_properties.update({curve_id:{}})

            for path in segment_group:
                data_type = path.split("/")[-1].split(".")[0]

                if data_type == 'segment-header':
                    with afm_file.read(bytes(path, 'utf-8')) as metadatacontents:
                        metadata_raw = bytes(metadatacontents).decode().splitlines()
                        # segment_metadata = jprops.load_properties(metadata_raw)
                        segment_metadata = {item.split("=")[0]:item.split("=")[1] for item in metadata_raw if not item.startswith("#")}
                        curve_properties = parseJPKsegmentheader(curve_properties, curve_id, filesuffix, segment_metadata, UFF._sharedataprops, segment_id)
        
        channels = curve_properties['0']['0']['channels']

        # Deflection channels
        found_vDeflection = "vDeflection"  in channels

        # Prioritize data obtained from the height sensor.
        if "measuredHeight" in channels: height_channel_key = "measuredHeight"
        elif "capacitiveSensorHeight" in channels: height_channel_key = "capacitiveSensorHeight"
        elif "height" in channels: height_channel_key = "height"
        else: height_channel_key = None

        UFF.filemetadata['found_vDeflection'] = found_vDeflection
        UFF.filemetadata['height_channel_key'] = height_channel_key

        UFF.filemetadata['curve_properties'] = curve_properties

    return UFF