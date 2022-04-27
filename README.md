# Pyafmreader V.x.x.x

In development, not stable.

If you have any questions, contact:
Javier.LOPEZ-ALONSO@ibl.cnrs.fr

## Installation
1. Download repository
2. Run python -m setup.py install

## Usage
```
from pyafmreader import loadfile

NANOSC_FV_PATH = 'tests/testfiles/20200903_Egel2.0_00023.spm'

NANOSC_SINGLE_CURVE_FILE = loadfile(NANOSC_SINGLE_CURVE_PATH)

metadata = NANOSC_SINGLE_CURVE_FILE.filemetadata

piezoimg = NANOSC_SINGLE_CURVE_FILE.getpiezoimg()

FC = NANOSC_SINGLE_CURVE_FILE.getcurve(0)

FC_segments = FC.get_segments()

segment_0 = FC_segments[0]
```