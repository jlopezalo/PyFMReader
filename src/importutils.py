import numpy as np

class Segment:
    def __init__(self, file_id, segment_id, segment_type):
        self.file_id = file_id
        self.segment_id = segment_id
        self.segment_type = segment_type
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
        Compute force vs indentation curve from deflection and piezo_height.

        Indentation = piezo_height(m) − deflection(m) − (piezo_height(CP)(m) − deflection(CP)(m))
        Force = Kc(N/m) * deflection(m)

        Reference: doi: 10.1002/jemt.22776

        Arguments:
        piezo_height -- z position of the piezo in m
        deflection -- deflection of the cantilever in m
        poc -- point of contact in m
        spring_constant -- spring constant of the cantilever in N/m

        Returns:
        List containing 2 arrays, where the first array is the indentation in m
        and the second array is the force in N.
        """
        # Set the center position to 0, 0 and get a force curve
        center_force_x = poc[0] - poc[1]
        center_force_y = poc[1] * spring_constant

        # Indentation = piezo_height(m) − deflection(m) − (piezo_height(CP)(m) − deflection(CP)(m))
        # Force = Kc(N/m) * deflection(m)
        self.indentation = np.array(self.zheight - self.vdeflection - center_force_x)
        self.force = np.array(self.zheight * spring_constant - center_force_y)


class ForceCurve:
    def __init__(self, curve_index, file_id):
        self.file_id = file_id
        self.curve_index = curve_index
        self.extend_segments = []
        self.retract_segments = []
        self.pause_segments = []
        self.modulation_segments = []

    def get_segments(self):
        force_curve_segments = [*self.extend_segments, *self.pause_segments, *self.modulation_segments, *self.retract_segments]
        return sorted(force_curve_segments, key=lambda x: int(x[0]))