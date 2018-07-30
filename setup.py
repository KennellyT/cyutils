from setuptools import setup
import io
import os

here = os.path.abspath(os.path.dirname(__file__))
def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')
VERSION = '0.1.1'

setup(
    name='cyutils',
    version=VERSION,
    url='http://github.com/KennellyT/cyutils/',
    license='BSD 3-Clause License',
    author='Tyler Kennelly',
    tests_require=['nose'],
    description='Cyclus analysis package.',
    long_description=long_description,
    packages=['cyutils',
              'cyutils.database',
              'cyutils.examples',
              'cyutils.sql_files',
              'cyutils.templates',
              ],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 3-Clause',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require={
        'testing': ['nose'],
    }
)
