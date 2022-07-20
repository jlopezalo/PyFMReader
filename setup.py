import os

os.system('python -m pip install Cython')

os.system('python -m pip install -e git+https://github.com/TkTech/fasterzip@09e2cae7821f96f4ba8f6d4122e1045352a656b4#egg=fasterzip')

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "pyafmreader",
    version= "x.x.x",
    description=None,
    long_description=long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    url="https://github.com/jlopezalo/pyafmreader",
    install_requires = [
        'Cython>=0.29.28',
        'numpy',
        'fasterzip @ git+https://github.com/TkTech/fasterzip.git'
    ]
)