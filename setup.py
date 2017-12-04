from setuptools import setup, find_packages
from ductus import __version__
import os

def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ductus',
    version=__version__,
    description="Helper classes for the ductus project",
    long_description=read_file('README.md'),
    keywords='bioinformatics',
    install_requires=[],
    author='IGP Platform, Uppsala University',
    packages=find_packages(),
    include_package_data=True
)
