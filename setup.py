from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "pyafmreader",
    version= "0.0.1",
    description=None,
    py_modules=["pyafmreader"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    url="https://github.com/jlopezalo/pyafmreader",
)