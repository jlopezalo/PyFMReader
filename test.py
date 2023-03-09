from pyafmreader.pyafmreader import loadfile

path = r'D:/Force curves dataset -FS on THP1 cells/Exp1/Cell1\\force-save-2021.01.22-17.57.23.079.jpk-force.zip'

file = loadfile(path)

print(file)