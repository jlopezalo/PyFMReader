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
        'Cython',
        'fasterzip @ git+https://github.com/TkTech/fasterzip.git#egg=fasterzip',
    ]
)