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
    entry_points={
        'console_scripts': [
            'rsync.py=ductus.scripts.rsync'
        ]
    },
    install_requires=[
        'cchardet'
    ],
    author='IGP Platform, Uppsala University',
    packages=find_packages(),
    include_package_data=True
)
