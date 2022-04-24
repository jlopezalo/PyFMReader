import os
import streamlit as st
from pathlib import Path
from pyafmreader import loadfile

def readfiles(path, savedir):
    for item in path.iterdir():
        if item.is_file():
            UFF = loadfile(str(item.absolute()))
            UFF.to_txt(savedir)
        elif item.is_dir():
            readfiles(item.absolute())

st.write(
"""
# Pyafmreader
### Supported file types:
- JPK Files: .jpk-force, .jpk-force-map, .jpk-qi-data
- Bruker Files: .spm, .pfc
"""
)

datapath = st.text_input("Enter a file or directory path:")

savedir = st.text_input("Output directory path:")

if st.button('Convert Files'):
    if os.path.isdir(savedir):
        readfiles(Path(datapath), savedir)
    else:
        raise NotADirectoryError