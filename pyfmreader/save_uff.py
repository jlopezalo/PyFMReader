import os

def saveUFFtxt(savefile, UFF, savedir, curveidx=0):
    """
    Save data and metadata into txt UFF files.

    If it is a Force Volume file, every force curve will be saved into an individual txt UFF file.

    The txt files are named as follows: 

        file_name.uff (for files containing single curves).

        file_name_curveidx.uff (for Force Volume files).

            Parameters:
                    savefile (str): Path to the save file.
                    UFF (uff.UFF): UFF object containing the data to save.
                    savedir (str): Path to the folder to save the txt UFF files.
                    curveidx (int): Index of the force distance curve to save.
            
            Returns: None
    """
    filemetadata = UFF.filemetadata
    if UFF.isFV:
        savefile = os.path.join(savedir, filemetadata['Entry_filename'] + f'_{curveidx}' + '.uff')
    else:
        savefile = os.path.join(savedir, filemetadata['Entry_filename'] + '.uff')
    FDC = UFF.getcurve(curveidx)
    with open(savefile, 'w', encoding='utf=8') as f:
        f.write("HE UFF_code:                        %6s\n" % (filemetadata.get('UFF_code', 0)))
        f.write("HE Entry_UFF_version:               %s\n" % (str(filemetadata.get('Entry_UFF_version', 0))))
        f.write("HE Entry_date:                      %10s\n" % (filemetadata.get('Entry_date', 0)))
        f.write("HE Entry_filename:                  %s\n" % (filemetadata.get('Entry_filename', 0)))
        f.write("HE Entry_tot_nb_curve:              %d\n" % (filemetadata.get('Entry_tot_nb_curve', 0)))
        # f.write("Entry_version %d\n" % (filemetadata.get('EN.version', 0)))
        # f.write("Entry_txt_byte_len %d\n" % (filemetadata.get('EN.txt_byte_len', 0)))
        f.write("HE Author_name:                     %s\n" % (filemetadata.get('Author_name', 0)))
        f.write("HE Author_doi:                      %s\n" % (filemetadata.get('Author_doi', 0)))
        # f.write("Author_citation_title %s\n" % (filemetadata.get('AU.citation_title', 0)))
        # f.write("Author_citation_jrnl %s\n" % (filemetadata.get('AU.citation_jrnl', 0)))
        # f.write("Author_citation_vol %s\n" % (filemetadata.get('AU.citation_vol', 0)))
        # f.write("Author_citation_page %s\n" % (filemetadata.get('AU.citation_page', 0)))
        f.write("HE Entity_sample_name:              %s\n" % (filemetadata.get('Entity_sample_name', 0)))
        f.write("HE Entity_sample_species:           %s\n" % (filemetadata.get('Entity_sample_species', 0)))
        f.write("HE Experimental_software_version:   %s\n" % (filemetadata.get('Experimental_software_version', 0)))
        f.write("HE Experimental_instrument:         %s\n" % (filemetadata.get('Experimental_instrument', 0)))
        f.write("HE Experimental_instrument_model:   %s\n" % (filemetadata.get('Experimental_instrument_model', 0)))
        f.write("HE Experimental_instrument_scanner: %s\n" % (filemetadata.get('Experimental_instrument_scanner', 0)))
        f.write("HE Cantilever_model:                %s\n" % (filemetadata.get('Cantilever_model', 0)))
        f.write("HE Cantilever_shape:                %s\n" % (filemetadata.get('Cantilever_shape', 0)))
        f.write("HE Cantilever_springK_calib_meth:   %s\n" % (filemetadata.get('Cantilever_springK_calib_meth', 0)))
        f.write("HE Cantilever_springK_used(N/m):    %E\n" % (filemetadata.get('Cantilever_springK_used(N/m)', 0)))
        f.write("HE Cantilever_springK_read(N/m):    %E\n" % (filemetadata.get('Cantilever_springK_read(N/m)', 0)))
        f.write("HE Cantilever_springK_nominal(N/m): %E\n" % (filemetadata.get('Cantilever_springK_nominal(N/m)', 0)))
        f.write("HE Cantilever_length(m):            %E\n" % (filemetadata.get('Cantilever_length(m)', 0)))
        f.write("HE Cantilever_width(m):             %E\n" % (filemetadata.get('Cantilever_width(m)', 0)))
        f.write("HE Cantilever_resonFq(Hz):          %E\n" % (filemetadata.get('Cantilever_resonFq(Hz)', 0)))
        f.write("HE Cantilever_Qfactor:              %f\n" % (filemetadata.get('Cantilever_Qfactor', 0)))
        f.write("HE Cantilever_Acoefficient_GCI(nN.s^1.3/m): %f\n" % (filemetadata.get('Cantilever_Acoefficient_GCI(nN.s^1.3/m)', 0)))
        f.write("HE Cantilever_mount_angle(deg):     %f\n" % (filemetadata.get('Cantilever_mount_angle(deg)', 0)))
        f.write("HE Tip_geometry:                    %s\n" % (filemetadata.get('Tip_geometry', 0)))
        f.write("HE Tip_half_angle(deg):             %E\n" % (filemetadata.get('Tip_half_angle(deg)', 0)))
        f.write("HE Tip_radius(m):                   %E\n" % (filemetadata.get('Tip_radius(m)', 0)))
        f.write("HE Tip_height(m):                   %E\n" % (filemetadata.get('Tip_height(m)', 0)))
        f.write("HE Recording_curve_id:              %d\n" % (curveidx))
        f.write("HE Recording_invols_calib_method:   %s\n" % (filemetadata.get('Recording_invols_calib_method', 0)))
        f.write("HE Recording_xposition(m):          %E\n" % (filemetadata.get('Recording_xposition(m)', 0)))
        f.write("HE Recording_yposition(m):          %E\n" % (filemetadata.get('Recording_yposition(m)', 0)))
        f.write("HE Recording_zpiezo_sens(m/V):      %E\n" % (filemetadata.get('Recording_zpiezo_sens(m/V)', 0)))
        f.write("HE Recording_inv_optical_lever_sens_read(m/V): %E\n" % (filemetadata.get('Recording_inv_optical_lever_sens_read(m/V)', 0)))
        f.write("HE Recording_inv_optical_lever_sens_used(m/V): %E\n" % (filemetadata.get('Recording_inv_optical_lever_sens_used(m/V)', 0)))
        f.write("HE Recording_number_segment:        %d\n" % (filemetadata.get('Recording_number_segment', 0)))
        f.write("HE Recording_Z_close_loop_on:       %s\n" % (filemetadata.get('Recording_Z_close_loop_on', 0)))
        f.write("HE Recording_XY_close_loop_on:      %s\n" % (filemetadata.get('Recording_XY_close_loop_on', 0)))
        writeUFFsegment(f, FDC)
        

def writeUFFsegment(f, FDC):
    """
    Write data and metadata from each segment of the force curve to the UFF text file.

            Parameters:
                    f (file object): txt file to write into.
                    FDC (utils.forcecurve.ForceCurve): Force Curve object containing segments to save.
            
            Returns: None
    """
    for segid, segment in FDC.get_segments():
        # Write segment header
        f.write("HE Recording_segment_%d_type:      %s\n" % (int(segid), segment.segment_type))
        f.write("HE Recording_segment_%d_code:      %s\n" % (int(segid), segment.segment_code))
        f.write("HE Recording_segment_%d_description: %s\n" % (int(segid), segment.description))
        f.write("HE Recording_segment_%d_force_setpoint_mode: %s\n" % (int(segid), segment.force_setpoint_mode))
        f.write("HE Recording_segment_%d_nb:        %d \n" % (int(segid), int(segid)))
        f.write("HE Recording_segment_%d_nb_point:  %d \n" % (int(segid), segment.nb_point))
        f.write("HE Recording_segment_%d_nb_col:    %d \n" % (int(segid), segment.nb_col))
        for colidx in range(segment.nb_col):
            f.write("HE Recording_segment_%d_col_%d_title: %s \n" % (int(segid), colidx, list(segment.segment_formated_data.keys())[colidx]))
            f.write("HE Recording_segment_%d_col_%d_unit:  %s \n" % (int(segid), colidx, list(segment.segment_formated_data.keys())[colidx]))
        f.write("HE Recording_segment_%d_sampling_rate(Hz): %E \n" % (int(segid), segment.sampling_rate))
        f.write("HE Recording_segment_%d_velocity(m/s): %E \n" % (int(segid), segment.velocity))
        f.write("HE Recording_segment_%d_force_setpoint(N): %E \n" % (int(segid), segment.force_setpoint))
        f.write("HE Recording_segment_%d_z_displacement(m): %E \n" % (int(segid), segment.z_displacement))
        # Write segment data
        for j in range(segment.nb_point):
            ndat = "%s %5d " % (segment.segment_code, int(segid))
            for k in range(segment.nb_col):
                ndat = ndat + "%15E " % (list(segment.segment_formated_data.values())[k][j])
            f.write(ndat + "\n")

def saveUFFhdf5():
    pass