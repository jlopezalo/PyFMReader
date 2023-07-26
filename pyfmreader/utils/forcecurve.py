# File containing the following classes:
# ForceCurve --------------------------------------------------
# Class used to store the data of the different force curves
# within a file.
# Includes the following methods:
# get_segments()
# preprocess_force_curve()
# get_force_vs_indentation()


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
    
    def preprocess_force_curve(self, deflection_sens, height_channel_key, y0=None):
        """
        Computes Vertical Deflection in m and populates the vdeflection, zheight 
        and time properties for each segment in the force curve.

        vDeflection(m) = (vDeflection(V) - baseline(V)) * deflection_sens(m/V)

        if y0 is not None:
            vDeflection(m) = (vDeflection(V) - y0(V)) * deflection_sens(m/V)

                Parameters:
                        deflection_sens (float): In m/V
                        height_channel_key (str): Dictionary key to find height data in self.segment_formated_data.
                        y0 (float): Manual offset for the vertical deflection, in Volts.
                
                Returns: None
        """
        for _, segment in self.get_segments():
            segment.preprocess_segment(deflection_sens, height_channel_key, y0)
    
    def shift_height(self):
        """
        Shifts the values of zheight using the last zheight value of the last retract segment.
        This operation is necessary to process JPK files.
        
        xzero(m) = last zheight value of last retract segment
        shifted zheight = xzero(m) − zheight(m)

                Parameters: None
                
                Returns: None
        """
        xzero = self.retract_segments[-1][-1].zheight[-1] # Maximum height
        for _, segment in self.get_segments():
                segment.zheight = xzero - segment.zheight
        
    def get_force_vs_indentation(self, poc, spring_constant):
        """
        Computes force vs indentation curve from deflection and piezo_height and populates
        the indentation and force properties for each segment in force curve.

        Indentation = piezo_height(m) − deflection(m) − (piezo_height(CP)(m) − deflection(CP)(m))
        Force = Kc(N/m) * deflection(m)

                Reference: DOI:10.1002/jemt.22776

                Parameters:
                        poc (list): [poc_x, poc_y] in meters
                        spring_constant (float): in N/m
                
                Returns: None
        """
        for _, segment in self.get_segments():
            segment.get_force_vs_indentation(poc, spring_constant)