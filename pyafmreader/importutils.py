# File containing the following classes:
# Segment --------------------------------------------------
# Class used to store the data and metadata of the different
# segments that form an AFM force curve.
# Includes the following methods:
# preprocess_segment()
# get_force_vs_indentation_curve()
# ForceCurve --------------------------------------------------
# Class used to store the data of the different force curves
# within a file.
# Includes the following methods:
# get_segments()

import numpy as np

class Segment:
    """
    Class used to store the data and metadata of the different
    segments that form an AFM force curve.

            Properties:
                    file_id (str): AFM File identifier
                    segment_id (str): Segment position in the ForceCurve (0, 1, 2, etc.)
                    segment_type (str): Type of segment (Approach, Retract, Pause, Modulation)
                    segment_code (str): Code to identify segment type (AP, RE, PA, MO)
                    description (str): Description of the segment.
                    nb_point (int): Number of data points in the segment.
                    force_setpoint_mode (str): Type of force setpoint (Relative, Absolute).
                    nb_col (int): Number of data channels. 
                    force_setpoint (float): Force setpoint (N).
                    velocity (float): Ramp speed (m/s).
                    sampling_rate (float): Sampling rate (Hz).
                    z_displacement (float): Displacement in z axis (m).
                    segment_metadata (dict): Additional metadata (optional).
                    segment_raw_data (dict): Segment raw data (optional)
                    segment_formated_data (dict): Formated segment data.
                    height_channel_key (str): Key to get the piezo height data from the segment_formated_data dict.
                    zheight (np.array): Piezo height (m)
                    vdeflection (np.array): Vertical deflection (m)
                    time (np.array): Time (s) (optional)
                    indentation (np.array): Indentation (m) (optional)
                    force (np.array): Force (N) (optional)
            
            Methods:
                    preprocess_segment
                    get_force_vs_indentation_curve

    """
    def __init__(self, file_id, segment_id, segment_type):
        self.file_id = file_id                  
        self.segment_id = segment_id            
        self.segment_type = segment_type
        self.segment_code = None        
        self.description = None                 
        self.nb_point = None                    
        self.force_setpoint_mode = None
        self.nb_col = None
        self.force_setpoint = None
        self.velocity = None
        self.sampling_rate = None
        self.z_displacement = None
        self.segment_metadata = None
        self.segment_raw_data = None
        self.segment_formated_data = None
        self.height_channel_key = None
        self.zheight = None
        self.vdeflection = None
        self.time = None
        self.indentation = None
        self.force = None

        if self.segment_type == 'Approach': self.segment_code = 'AP'
        elif self.segment_type == 'Retract': self.segment_code = 'RE'
        elif self.segment_type == 'Pause': self.segment_code = 'PA'
        elif self.segment_type == 'Modulation': self.segment_code = 'MO'
    
    def preprocess_segment(self, deflection_sens, height_channel_key, y0=None):
        """
        Computes Vertical Deflection in m and populates the vdeflection, zheight 
        and time properties.

        vDeflection(m) = (vDeflection(V) - baseline(V)) * deflection_sens(m/V)

        if y0 is not None:
            vDeflection(m) = (vDeflection(V) - y0(V)) * deflection_sens(m/V)

                Parameters:
                        deflection_sens (float): In m/V
                        height_channel_key (str): Dictionary key to find height data in self.segment_formated_data.
                        y0 (float): Manual offset for the vertical deflection, in Volts.
                
                Returns: None
        """
        deflection_v = self.segment_formated_data["vDeflection"]
        if self.segment_metadata["baseline_measured"]:
            deflection_v = deflection_v - self.segment_metadata["baseline"]
        elif y0 is not None:
            deflection_v = deflection_v - y0
        self.vdeflection = deflection_v * deflection_sens
        self.zheight = self.segment_formated_data[height_channel_key]
        self.time = self.segment_formated_data["time"]
    
    def get_force_vs_indentation_curve(self, poc, spring_constant):
        """
        Computes force vs indentation curve from deflection and piezo_height and populates
        the indentation and force properties.

        Indentation = piezo_height(m) − deflection(m) − (piezo_height(CP)(m) − deflection(CP)(m))
        Force = Kc(N/m) * deflection(m)

                Reference: DOI:10.1002/jemt.22776

                Parameters:
                        poc (list): [poc_x, poc_y] in meters
                        spring_constant (float): in N/m
                
                Returns: None
        """
        # Set the center position to 0, 0 and get a force curve
        center_force_x = poc[0] - poc[1]
        center_force_y = poc[1] * spring_constant

        # Indentation = piezo_height(m) − deflection(m) − (piezo_height(CP)(m) − deflection(CP)(m))
        # Force = Kc(N/m) * deflection(m)
        self.indentation = np.array(self.zheight - self.vdeflection - center_force_x)
        self.force = np.array(self.zheight * spring_constant - center_force_y)


class ForceCurve:
    """
    Class used to store the data of the different force curves
    within a file.

            Properties:
                    file_id (str): AFM File identifier
                    curve_index (str): Curve position in the AFM File (0, 1, 2, etc.)
                    extend_segments (list): List containing approach segments.
                    retract_segments (list): List containing retract segments.
                    pause_segments (list): List containing pause segments.
                    modulation_segments (list): List containing modulation segments.
            
            Methods:
                    get_segments
    """
    def __init__(self, curve_index, file_id):
        self.file_id = file_id
        self.curve_index = curve_index
        self.extend_segments = []
        self.retract_segments = []
        self.pause_segments = []
        self.modulation_segments = []

    def get_segments(self):
        """
        Get all the force curve segments ordered by their segment id.

                Parameters: None
                
                Returns: List containing all the force curve segments sorted by their segment id.
        """
        force_curve_segments = [
            *self.extend_segments, *self.pause_segments, *self.modulation_segments, *self.retract_segments
        ]
        return sorted(force_curve_segments, key=lambda x: int(x[0]))