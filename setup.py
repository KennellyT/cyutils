from setuptools import setup
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.1.1'

setup(
    name='cyutils',
    VERSION='0.1.0',
    author='Tyler Kennelly',
    tests_require=['nose'],
    author_email='kennlly2@illinois.edu',
    packages=['cyutils', 'cyutils.test'],
    license='LICENSE.txt',
    description='Cyclus analysis package',
    long_description=open('README.rst').read()
    packages=['cyutils',
              'cyutils.cywrite',
              'cyutils.cyanalysis',
              'cyutils.templates',
              'cyutils.sql_files',
              'cyutils.database'
              ],
    classifiers=[
        'Development Status :: 1 - Developing',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 3-Clause',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Nuclear Fuel Cycle'
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    extras_require={
        'testing': ['nose'],
    }

)
