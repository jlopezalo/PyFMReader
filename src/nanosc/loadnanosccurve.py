import numpy as np
from struct import unpack
from importutils import ForceCurve, Segment
from constants import NANOSC_NB_COLS

def loadNANOSCcurve(idx, header):
    file_name = header['Entry_filename']
    filepath = header['file_path']
    force_curve = ForceCurve(idx, file_name)
    # Only simple curves with trace/retrace are supported
    appsegment = Segment(file_name, '0', 'Approach')
    retsegment = Segment(file_name, '1', 'Retract')
    with open(filepath, 'rb') as afmfile:
        # Get variables needed for loading data from header
        isFV = bool(header['force_volume'])
        isPFC = bool(header['peakforce'])
        FDC_data_length = header['FDC_data_length']
        FDC_nb_sampsline = header['FDC_nb_sampsline']
        nb_point_approach = header['nb_point_approach']
        nb_point_retract = header['nb_point_retract']
        data_offset = header['data_offset']
        zstep_approach_nm = header['zstep_approach_nm']
        zstep_retract_nm = header['zstep_retract_nm']
        defl_sens_Vbybyte = header['defl_sens_Vbybyte']
        PFC_freq = header['PFC_freq'] * 1000
        PFC_amp = header['PFC_amp']
        PFC_nb_samppoints = header['PFC_nb_samppoints']
        QNM_sync_dist = header['QNM_sync_dist']

        app_x =  np.arange(nb_point_approach) * zstep_approach_nm
        ret_x =  np.arange(nb_point_retract) * zstep_retract_nm

        tempapp = np.zeros((nb_point_approach))
        tempret = np.zeros((nb_point_retract))

        if isFV:
            FDC_bytes = FDC_data_length // (2 * nb_point_approach * FDC_nb_sampsline ** 2)
        else:
            FDC_bytes = FDC_data_length // (2 * nb_point_approach)

        if FDC_bytes == 2: fmt = 'h' # Short Int
        elif FDC_bytes == 4: fmt = 'i' # Int

        offset = int(data_offset + (idx * (nb_point_approach + nb_point_retract) * FDC_bytes))

        afmfile.seek(offset, 0)

        tempapp[:] = unpack(f"<{str(nb_point_approach)}{fmt}", afmfile.read(FDC_bytes * nb_point_approach))

        tempret[:] = unpack(f"<{str(nb_point_retract)}{fmt}", afmfile.read(FDC_bytes * nb_point_retract))

        if isPFC:

            f_samples = nb_point_approach

            if f_samples != PFC_nb_samppoints:
                pft_factor = PFC_nb_samppoints / (2 * f_samples)
                QNM_sync_dist = QNM_sync_dist / pft_factor

            curve_pft = np.zeros([2 * f_samples])
            curve_pft = np.concatenate((tempapp[::-1], tempret))
            max_force_index = np.argmax(curve_pft)
            sd = QNM_sync_dist / (PFC_freq * 2 * nb_point_approach)
            deltat = sd - 1 / (PFC_freq * 4)
            curve_t = np.arange(2 * nb_point_approach) * ((0.5 / PFC_freq) / nb_point_approach)
            curve_x = PFC_amp * np.sin(2 * np.pi * PFC_freq * (curve_t - deltat))

            app_x = curve_x[:max_force_index]
            tempapp = curve_pft[:max_force_index]
            
            ret_x = curve_x[(max_force_index):(max_force_index + f_samples)]
            tempret = curve_pft[(max_force_index):(max_force_index + f_samples)]


        app_defl_V = defl_sens_Vbybyte * tempapp
        ret_defl_V = defl_sens_Vbybyte * tempret

        start_pos = 0
        for i in range(len(app_defl_V)):
            if np.abs(app_defl_V[i] / app_defl_V[i+1]) > 10:
                continue
            else:
                start_pos = i
                break
            
        app_x = app_x[start_pos:]
        app_defl_V = app_defl_V[start_pos:] - ret_defl_V[-1]
        ret_defl_V = ret_defl_V - ret_defl_V[-1]

        if not isPFC:
            app_defl_V = app_defl_V[::-1]
            ret_defl_V = ret_defl_V[::-1]

        appsegment.segment_formated_data = {
                'height': app_x, 
                'vDeflection': app_defl_V
            }

        retsegment.segment_formated_data = {
            'height': ret_x, 
            'vDeflection': ret_defl_V
        }

        appsegment.nb_point = len(app_x)
        appsegment.force_setpoint_mode = header['trigger_mode']
        appsegment.nb_col = NANOSC_NB_COLS
        appsegment.force_setpoint = 0
        appsegment.velocity = header['speed_forward_nmbys']
        appsegment.sampling_rate = header['scan_rate_Hz']
        appsegment.z_displacement = header['ramp_size_nm']

        retsegment.nb_point = len(ret_x)
        retsegment.force_setpoint_mode = header['FDC_data_length']
        retsegment.nb_col = NANOSC_NB_COLS
        retsegment.force_setpoint = 0
        retsegment.velocity = header['speed_forward_nmbys']
        retsegment.sampling_rate = header['scan_rate_Hz']
        retsegment.z_displacement = header['ramp_size_nm']

        force_curve.extend_segments.append((0, appsegment))
        force_curve.retract_segments.append((1, retsegment))

        return force_curve