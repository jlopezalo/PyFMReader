import streamlit as st
from pyafmreader import loadfile

st.write(
"""
# Pyafmreader
### Supported file types:
- JPK Files: .jpk-force, .jpk-force-map, .jpk-qi-data
- Bruker Files: .spm, .pfc
"""
)

filename = st.text_input("Enter a file path:")

uff = loadfile(filename)