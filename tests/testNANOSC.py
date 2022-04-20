import matplotlib.pyplot as plt

from pyafmreader import loadfile

# test_file = '/Users/javierlopez/Desktop/Stuff/My_projects/afm-rheology/test_files/Nano_Au_Box_2_Sample3_00000spm.0_00022.spm'
test_file = '/Users/javierlopez/Desktop/Data Javier/08171528.0_00001.pfc'

file = loadfile(test_file)

print(file.filemetadata)

piezoimg = file.getpiezoimg()

plt.imshow(piezoimg, cmap='afmhot', origin='lower')
plt.show()

fdc = file.getcurve(0)
fdcsegs = fdc.get_segments()