from setuptools import setup
from distutils.core import setup

VERSION = '0.1.1'

setup( 
   name='cyutils',
   VERSION='0.1.0',
   author='Tyler Kennelly',
   author_email='kennlly2@illinois.edu',
   packages=['cyutils', 'cyutils.test'],
   license='LICENSE.txt',
   description='Cyclus analysis package',
   long_description=open('README.rst').read()
   
)
