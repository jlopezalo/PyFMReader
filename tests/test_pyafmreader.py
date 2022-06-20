# Unit tests for the pyafmreader module.

# NOT FINISHED!!!

import unittest
from pyafmreader import loadfile

class TestPyafmreader(unittest.TestCase):

    def setUp(self):
        # Declare paths to test files
        JPK_SINGLE_CURVE_PATH = 'tests/testfiles/force-save-2020.12.04-14.39.51.983.jpk-force'
        JPK_FV_PATH = None
        JPK_QI_PATH = None
        NANOSC_SINGLE_CURVE_PATH = 'tests/testfiles/20200904_Egel4-Z1.0_00025.spm'
        NANOSC_FV_PATH = 'tests/testfiles/20200903_Egel2.0_00023.spm'
        NANOSC_PFC_PATH = 'tests/testfiles/08171528.0_00001.pfc'
        UFF_PATH = 'tests/testfiles/20200904_Egel4-Z1.0_00025.uff'
        # JPK files
        self.JPK_SINGLE_CURVE_FILE = None
        self.JPK_FV_FILE = None
        self.JPK_QI_FILE = None
        # NANOSCOPE files
        self.NANOSC_SINGLE_CURVE_FILE = loadfile(NANOSC_SINGLE_CURVE_PATH)
        self.NANOSC_FV_FILE = loadfile(NANOSC_FV_PATH)
        self.NANOSC_PFC_FILE = loadfile(NANOSC_PFC_PATH)
        # UFF files
        self.UFF_FILE = loadfile(UFF_PATH)

    def test_load_NANOSC_single_curve_header(self):
        metadata = self.NANOSC_SINGLE_CURVE_FILE.filemetadata
        self.assertEqual(metadata.get('Entry_filename', None), '20200904_Egel4-Z1.0_00025.spm')
        self.assertEqual(metadata.get('file_type', None), '.spm')
        self.assertEqual(metadata.get('version', None), '0x0920B046')
        self.assertEqual(metadata.get('zscan_sens_nmbyV', None), 13.203)
        self.assertEqual(metadata.get('instru', None), 'MultiMode 8')
        self.assertEqual(metadata.get('scanner', None), '10776jvlr_20200108_5V.scn')
        self.assertEqual(metadata.get('force_volume', None), 0)
        self.assertEqual(metadata.get('xoffset_nm', None), 0)
        self.assertEqual(metadata.get('yoffset_nm', None),0)
        self.assertEqual(metadata.get('defl_sens_nmbyV', None), 27.39000)
        self.assertEqual(metadata.get('xy_closed_loop', None), 'Off')
        self.assertEqual(metadata.get('z_closed_loop', None), 'Off')
        self.assertEqual(metadata.get('peakforce', None), 0)
        self.assertEqual(metadata.get('PFC_amp', None), 100)
        self.assertEqual(metadata.get('PFC_freq', None), 2)
        self.assertEqual(metadata.get('PFC_nb_samppoints', None), 128)
        self.assertEqual(metadata.get('NEW_sync_dist', None), 0)
        self.assertEqual(metadata.get('QNM_sync_dist', None), 0)
        self.assertEqual(metadata.get('piezo_nb_sampsline', None), 256)
        self.assertEqual(metadata.get('sens_z_sensor', None), 906.4730)
        self.assertEqual(metadata.get('trigger_mode', None), 'Relative')
        self.assertEqual(metadata.get('FDC_nb_sampsline', None), 16)
        self.assertEqual(metadata.get('scan_rate_Hz', None), 1.01725)
        self.assertEqual(metadata.get('speed_forward_Vbys', None), 462.282)
        self.assertEqual(metadata.get('speed_reverse_Vbys', None), 462.282)
        self.assertEqual(metadata.get('defl_sens_Vbybyte', None), 0.000375)
        self.assertEqual(metadata.get('defl_sens_corr', None), 1.08)
        self.assertEqual(metadata.get('nb_point_approach', None), 1024)
        self.assertEqual(metadata.get('nb_point_retract', None), 1024)
        self.assertEqual(metadata.get('spring_const_Nbym', None), 0.1332)
        self.assertEqual(metadata.get('FDC_data_length', None), 8192)
        self.assertEqual(metadata.get('data_offset', None), 80960)
        self.assertEqual(metadata.get('byte_per_pixel', None), 2)
        self.assertEqual(metadata.get('z_scale_Vbybyte', None), 0.0003750000)
        self.assertEqual(metadata.get('ramp_size_V', None), 0.006713765)
        self.assertEqual(metadata.get('FV_data_length', None), None)
        self.assertEqual(metadata.get('FV_nb_sampsline', None), None)
        self.assertEqual(metadata.get('FV_nb_lines', None), None)
        self.assertEqual(metadata.get('FV_ima_offset', None), None)
        self.assertEqual(metadata.get('FV_ima_scanX', None), None)
        self.assertEqual(metadata.get('FV_ima_scanY', None), None)
        self.assertEqual(metadata.get('FV_Zsens', None), None)
        self.assertEqual(metadata.get('bytes_per_pxl', None), None)


    def test_load_NANOSC_FV_header(self):
        metadata = self.NANOSC_FV_FILE.filemetadata
        self.assertEqual(metadata.get('Entry_filename', None), '20200903_Egel2.0_00023.spm')
        self.assertEqual(metadata.get('file_type', None), '.spm')
        self.assertEqual(metadata.get('version', None), '0x0920B046')
        self.assertEqual(metadata.get('zscan_sens_nmbyV', None), 13.203)
        self.assertEqual(metadata.get('instru', None), 'MultiMode 8')
        self.assertEqual(metadata.get('scanner', None), '10776jvlr_20200108_5V.scn')
        self.assertEqual(metadata.get('force_volume', None), 1)
        self.assertEqual(metadata.get('xoffset_nm', None), 0)
        self.assertEqual(metadata.get('yoffset_nm', None),0)
        self.assertEqual(metadata.get('defl_sens_nmbyV', None), 27.39000)
        self.assertEqual(metadata.get('xy_closed_loop', None), 'Off')
        self.assertEqual(metadata.get('z_closed_loop', None), 'Off')
        self.assertEqual(metadata.get('peakforce', None), 0)
        self.assertEqual(metadata.get('PFC_amp', None), 100)
        self.assertEqual(metadata.get('PFC_freq', None), 2)
        self.assertEqual(metadata.get('PFC_nb_samppoints', None), 128)
        self.assertEqual(metadata.get('NEW_sync_dist', None), 0)
        self.assertEqual(metadata.get('QNM_sync_dist', None), 0)
        self.assertEqual(metadata.get('piezo_nb_sampsline', None), 16)
        self.assertEqual(metadata.get('sens_z_sensor', None), 906.4730)
        self.assertEqual(metadata.get('trigger_mode', None), 'Relative')
        self.assertEqual(metadata.get('FDC_nb_sampsline', None), 16)
        self.assertEqual(metadata.get('scan_rate_Hz', None), 1.01725)
        self.assertEqual(metadata.get('speed_forward_Vbys', None), 308.188)
        self.assertEqual(metadata.get('speed_reverse_Vbys', None), 308.188)
        self.assertEqual(metadata.get('defl_sens_Vbybyte', None), 0.000375)
        self.assertEqual(metadata.get('defl_sens_corr', None), 1.08)
        self.assertEqual(metadata.get('nb_point_approach', None), 1024)
        self.assertEqual(metadata.get('nb_point_retract', None), 1024)
        self.assertEqual(metadata.get('spring_const_Nbym', None), 0.1332)
        self.assertEqual(metadata.get('FDC_data_length', None), 2097152)
        self.assertEqual(metadata.get('data_offset', None), 80960)
        self.assertEqual(metadata.get('byte_per_pixel', None), 2)
        self.assertEqual(metadata.get('z_scale_Vbybyte', None), 0.0003750000)
        self.assertEqual(metadata.get('ramp_size_V', None), 0.006713765)
        self.assertEqual(metadata.get('FV_data_length', None), 1024)
        self.assertEqual(metadata.get('FV_nb_sampsline', None), 16)
        self.assertEqual(metadata.get('FV_nb_lines', None), 16)
        self.assertEqual(metadata.get('FV_ima_offset', None), 2178112)
        self.assertEqual(metadata.get('FV_ima_scanX', None), 2e-06)
        self.assertEqual(metadata.get('FV_ima_scanY', None), 2e-06)
        self.assertEqual(metadata.get('FV_Zsens', None), 0.006713765)
        self.assertEqual(metadata.get('bytes_per_pxl', None), 2)

    def test_load_NANOSC_PFC_header(self):
        metadata = self.NANOSC_PFC_FILE.filemetadata
        self.assertEqual(metadata.get('Entry_filename', None), '08171528.0_00001.pfc')
        self.assertEqual(metadata.get('file_type', None), '.pfc')
        self.assertEqual(metadata.get('version', None), '0x0940B020')
        self.assertEqual(metadata.get('zscan_sens_nmbyV', None), 29.12)
        self.assertEqual(metadata.get('instru', None), 'BioScope Resolve')
        self.assertEqual(metadata.get('scanner', None), 'beta1_beta1.scn')
        self.assertEqual(metadata.get('force_volume', None), 1)
        self.assertEqual(metadata.get('xoffset_nm', None), 203.125)
        self.assertEqual(metadata.get('yoffset_nm', None), -351.563)
        self.assertEqual(metadata.get('defl_sens_nmbyV', None), 10.0)
        self.assertEqual(metadata.get('xy_closed_loop', None), 'Off')
        self.assertEqual(metadata.get('z_closed_loop', None), 'On')
        self.assertEqual(metadata.get('peakforce', None), 1)
        self.assertEqual(metadata.get('PFC_amp', None), 10.0)
        self.assertEqual(metadata.get('PFC_freq', None), 2)
        self.assertEqual(metadata.get('PFC_nb_samppoints', None), 256)
        self.assertEqual(metadata.get('NEW_sync_dist', None), 88)
        self.assertEqual(metadata.get('QNM_sync_dist', None), 89)
        self.assertEqual(metadata.get('piezo_nb_sampsline', None), 256)
        self.assertEqual(metadata.get('sens_z_sensor', None), 156.4861)
        self.assertEqual(metadata.get('trigger_mode', None), 'Relative')
        self.assertEqual(metadata.get('FDC_nb_sampsline', None), 256)
        self.assertEqual(metadata.get('scan_rate_Hz', None), 81.3802)
        self.assertEqual(metadata.get('speed_forward_Vbys', None), 242.165)
        self.assertEqual(metadata.get('speed_reverse_Vbys', None), 242.165)
        self.assertEqual(metadata.get('defl_sens_Vbybyte', None), 0.000375)
        self.assertEqual(metadata.get('defl_sens_corr', None), 1.08)
        self.assertEqual(metadata.get('nb_point_approach', None), 128)
        self.assertEqual(metadata.get('nb_point_retract', None), 128)
        self.assertEqual(metadata.get('spring_const_Nbym', None), 0.09)
        self.assertEqual(metadata.get('FDC_data_length', None), 67108864)
        self.assertEqual(metadata.get('data_offset', None), 343104)
        self.assertEqual(metadata.get('byte_per_pixel', None), 2)
        self.assertEqual(metadata.get('z_scale_Vbybyte', None), 0.0003750000)
        self.assertEqual(metadata.get('ramp_size_V', None), 0.0007104712)
        self.assertEqual(metadata.get('FV_data_length', None), 262144)
        self.assertEqual(metadata.get('FV_nb_sampsline', None), 256)
        self.assertEqual(metadata.get('FV_nb_lines', None), 256)
        self.assertEqual(metadata.get('FV_ima_offset', None), 80960)
        self.assertEqual(metadata.get('FV_ima_scanX', None), 2e-06)
        self.assertEqual(metadata.get('FV_ima_scanY', None), 2e-06)
        self.assertEqual(metadata.get('FV_Zsens', None), 5.72205e-09)
        self.assertEqual(metadata.get('bytes_per_pxl', None), 4)

    def test_load_JPK_single_curve_header(self):
        pass

    def test_load_JPK_FV_header(self):
        pass

    def test_load_JPK_QI_header(self):
        pass

    def test_load_UFF_header(self):
        pass

if __name__ == '__main__':
    unittest.main()