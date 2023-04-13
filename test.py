from pyafmreader.pyafmreader import loadfile

path = r'C:\Users\javier.lopez\OneDrive - Optics11 BV\Desktop\map-data-2021.03.21-14.22.37.755.jpk-force-map'

file = loadfile(path)

file.getcurve(0)

print(file)