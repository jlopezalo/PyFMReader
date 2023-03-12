from pyafmreader.pyafmreader import loadfile

path = r'C:\Users\javier.lopez\Documents\Datasets\191209_Microrheology_THP1_PLL_mltcbioE\force-save-2019.12.09-15.20.07.822.jpk-force.zip'

file = loadfile(path)

file.getcurve(0)

print(file)