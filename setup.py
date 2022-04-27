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
        'fasterzip @ git+https://github.com/TkTech/fasterzip.git@09e2cae7821f96f4ba8f6d4122e1045352a656b4#egg=fasterzip',
    ]
)