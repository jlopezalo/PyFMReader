import os
import re

def getstring(line):
    return line.strip('\r\n').split(': ')[1]

def getfloat(line):
    _, nf = line.strip('\r\n').split(': ', 1)
    return float(re.findall(r'([0-9][.][0-9]+|[0-9]+)', nf)[0])

def getint(line):
    _, nf = line.strip('\r\n').split(': ', 1)
    return int(re.findall(r'([0-9][.][0-9]+|[0-9]+)', nf)[0])

def parseNANOSCheader(filepath):
    header = {}
    position = None
    data_offset_found_flag = False
    header["file_path"] = filepath
    header["file_name"] = os.path.basename(filepath)
    header["file_size_bytes"] = os.path.getsize(filepath)
    header["file_type"] = os.path.splitext(filepath)[-1]
    
    with open(filepath, 'rb') as afmfile:
        headerlines = afmfile.readlines()
        for rawline in headerlines:
            line = rawline.decode('latin_1')

            # End of header flag
            if '\\*File list end' in line:
                break
            
            # Header positions
            elif '*Ciao scan list' in line:
                position = 'ScanList'
            elif '*Ciao force list' in line:
                position = 'ForceList'
            elif '*Ciao force image list' in line:
                position = 'ForceÍmageList'
            elif '*Ciao image list' in line:
                position = 'ImageList'
            elif '\\Version:' in line:
                header['version'] = getstring(line)
            elif '\\@Sens. Zsens:' in line or '\\@Sens. Zscan:' in line:
                header['zscan_sens_nmbyV'] = getfloat(line)
            elif '\\Microscope:' in line:
                header['instru'] = getstring(line)
            elif '\\Scanner file:' in line:
                header['scanner'] = getstring(line)
            
            # ScanList position fields
            if position == 'ScanList':
                if '\\Operating mode:' in line:
                    if getstring(line) in ('Force Volume', 'Image'):
                        header['force_volume'] = 1
                    else:
                        header['force_volume'] = 0
                elif '\\X Offset:' in line:
                    header['xoffset_nm'] = getfloat(line)
                elif '\\Y Offset:' in line:
                    header['yoffset_nm'] = getfloat(line)
                elif '\\@Sens. DeflSens:' in line or '\\@Sens. Deflection:' in line:
                    header['defl_sens_nmbyV'] = getfloat(line)
                elif '\\XY Closed Loop:' in line:
                    header['xy_closed_loop'] = getstring(line)
                elif '\\Z Closed Loop:' in line:
                    header['z_closed_loop'] = getstring(line)
                elif '\\PeakForce Capture:' in line:
                    if getstring(line) == 'Allow':
                        header['peakforce'] = 1
                    else:
                        header['peakforce'] = 0
                elif '\\Peak Force Amplitude:' in line:
                    header['PFC_amp'] = getfloat(line)
                elif '\\PFT Freq:' in line:
                    header['PFC_freq'] = getfloat(line)
                elif '\\Sample Points:' in line:
                    header['PFC_nb_samppoints'] = getint(line)
                elif '\\Sync Distance New:' in line:
                    header['NEW_sync_dist'] = getint(line)
                elif '\\Sync Distance QNM:' in line:
                    header['QNM_sync_dist'] = getint(line)
                elif '\\Samps/line:' in line:
                    header['piezo_nb_sampsline'] = getint(line)
                elif '\\@Sens. ZsensSens:' in line:
                    header['sens_z_sensor'] = getfloat(line)
            
            # ForceList position fields
            elif position == 'ForceList':
                if '\\Trigger mode:' in line:
                    header['trigger_mode'] = getstring(line)
                elif '\\force/line' in line:
                    header['FDC_nb_sampsline'] = getint(line)
                elif '\\Scan rate:' in line:
                    header['scan_rate_Hz'] = getfloat(line)
                elif '\\Forward vel.:' in line:
                    header['speed_forward_Vbys'] = getfloat(line)
                elif '\\Reverse vel.:' in line:
                    header['speed_reverse_Vbys'] = getfloat(line)
                elif '\\@4:Trig threshold Deflection:' in line or\
                     '\\@4:Trig Threshold Deflection:' in line:
                    header['defl_sens_Vbybyte'] = getfloat(line)
                elif '\\Deflection Sensitivity Correction:' in line:
                    header['defl_sens_corr'] = getfloat(line)
                elif '\\Samps/line:' in line:
                    _, nf = line.strip('\r\n').split(': ', 1)
                    nbptret, nbptapp = re.findall(r'([0-9][.][0-9]+|[0-9]+)', nf)
                    header['nb_point_approach'] = int(nbptapp)
                    header['nb_point_retract'] = int(nbptret)
            
            #  ForceÍmageList position fields
            elif position == 'ForceÍmageList':
                if '\\Spring Constant:' in line or\
                   '\\Spring constant:' in line:
                   header['spring_const_Nbym'] = getfloat(line)
                elif '\\Data length:' in line:
                    header['FDC_data_length'] = getint(line)
                elif '\\Data offset:' in line and not data_offset_found_flag:
                    header['data_offset'] = getint(line)
                    data_offset_found_flag = True
                elif '\\Bytes/pixel:' in line:
                    header['byte_per_pixel'] = getint(line)
                elif '\\@4:Z scale: V [Sens. DeflSens]' in line:
                    header['z_scale_Vbybyte'] = getfloat(line)
                elif '\\@4:FV scale: V [Sens. ZsensSens]' in line:
                    header['z_scale_Vbybyte'] = getfloat(line)
                elif '\\@4:Ramp size:' in line or\
                     '\\@4:Ramp Size:' in line:
                    header['ramp_size_V'] = getfloat(line)
            
            # ImageList position fields
            elif position == 'ImageList':
                if '\\Data length' in line:
                    header['FV_data_length'] = getint(line)
                elif '\\Samps/line:' in line:
                    header['FV_nb_sampsline'] = getint(line)
                elif '\\Number of lines:' in line:
                    header['FV_nb_lines'] = getint(line)
                elif '\\Data offset:' in line:
                    header['FV_ima_offset'] = getint(line)
                elif '\\Scan Size:' in line:
                    _, nf = line.strip('\r\n').split(': ', 1)
                    units = re.findall(r'([a-z\~]+)', nf)[0]
                    x, y = re.findall(r'([0-9][.][0-9]+|[0-9]+)', nf)
                    if units == 'nm': mult = 1E-9
                    elif units == '~m': mult = 1E-6
                    header['FV_ima_scanX'] = float(x) * mult
                    header['FV_ima_scanY'] = float(y) * mult
                elif '\\@2:Z scale:' in line:
                    header['FV_Zsens'] = getfloat(line)
                elif '\\Bytes/pixel' in line:
                    header['bytes_per_pxl'] = getint(line)
        
        # Compute parameters not stored in header
        if header['force_volume'] == 1:
            header['tot_nb_FDC'] = header['FV_nb_sampsline'] * header['FV_nb_lines']
        else:
            header['tot_nb_FDC'] = 1
        header['ramp_size_nm'] = header['ramp_size_V'] * header['zscan_sens_nmbyV']
        header['speed_forward_nmbys'] = header['speed_forward_Vbys'] * header['zscan_sens_nmbyV']
        header['speed_reverse_nmbys'] = header['speed_reverse_Vbys'] * header['zscan_sens_nmbyV']
        header['zstep_approach_nm'] = header['ramp_size_nm'] / header['nb_point_approach']
        header['zstep_retract_nm'] = header['ramp_size_nm'] / header['nb_point_retract']
    
    return header