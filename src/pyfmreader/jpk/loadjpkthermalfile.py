import os
import pandas as pd

def loadJPKThermalFile(file_path):
    # Get the file extension to make sure it is
    # a .tnd file.
    file_ext  = os.path.splitext(file_path)[1]
    if file_ext == ".tnd":
        # On the current version the header of
        # JPK thermal files consists of 23 rows.
        header_rows = 23
        # Read header
        file_header = pd.read_csv(file_path, header=None, nrows=header_rows)
        parameters = {}
        for value in file_header[0]:
            param_data = value.replace('# ', '').split(': ')
            # print(value.replace('# ', '').split(': '))
            # Skip rows with only one element.
            # These are normally rows containing titles for
            # sections of the file, like: thermal noise data
            if len(param_data) == 1:
                continue
            # Split in param key and value
            param_key, param_val = param_data
            try:
                # Split units from param value
                param_val, param_units = param_val.split(' ')
                # Scale all params
                mult = 1
                if param_units[0] == 'k': mult = 1e3
                elif param_units[0] in 'm': mult = 1e-3
                elif param_units[0] == 'µ': mult = 1e-6
                elif param_units[0] in 'n': mult = 1e-9
                parameters[param_key] = float(param_val) * mult
            except ValueError:
                # Some values can not be transformed to floats
                # due to their notation or because they are not
                # numeric. If that is the case a ValueError
                # exception is raised by python.
                parameters[param_key] = param_val
        # The different data columns are determined
        # by blank spaces.
        data_sep = ' '
        # Read data
        file_data = pd.read_csv(
            file_path, sep=data_sep, comment='#',
            names = ['Frequency', 'Vertical Deflection', 'average', 'fit-data'],
            engine='python')
        # Compute amplitude in m^2/Hz
        # Data in vile is saved in V^2/Hz
        # V^2/Hz * invOLS^2(m^2/V^2) = m^2/Hz
        ampl_raw = file_data['average'].values  # V^2/Hz
        ampl_scaled = ampl_raw * parameters['sensitivity'] ** 2 # m^2/Hz
        # Get frequency values
        freq = file_data['Frequency'].values # Hz
        # Get fit values in  m^2/V
        # There may be no fit data in the file,
        # if that is the case python will raise
        # a KeyError exception.
        try:
            fit_data = (file_data['fit-data'] * parameters['sensitivity'] ** 2).values
        except KeyError:
            fit_data = None
        return ampl_raw, ampl_scaled, freq, fit_data, parameters