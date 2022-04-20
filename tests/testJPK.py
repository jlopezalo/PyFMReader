import matplotlib.pyplot as plt

from pyafmreader import loadfile

# 100 MB file
test_file = '/Users/javierlopez/Desktop/QI_/QI_pepg-1.jpk-qi-data'

file = loadfile(test_file)

# print(file.filemetadata)

piezoimg = file.getpiezoimg()

plt.imshow(piezoimg, cmap='afmhot', origin='lower')
plt.show()

fdc = file.getcurve(0)
# fdcsegs = fdc.get_segments()

# for segid, seg in fdcsegs:
#     deflsens = file.filemetadata['original_deflection_sensitivity'] / 1e9
#     height_channel_key = file.filemetadata['height_channel_key']
#     seg.preprocess_segment(deflsens, height_channel_key)
#     plt.plot(seg.zheight * 1e9, seg.vdeflection * 1e9)
# plt.show()