'''
Created on Mar 1, 2019

@author: geomatics
'''
from distutils.core import setup
from Cython.Build import cythonize
path = '/home/geomatics/eclipse-workspace/SatWare_v018/SatWare_v017/GNSS/FileReaders2.pyx'

setup(ext_modules = cythonize(path))