from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("*.pyx")
)

#python3 cython_test.py build_ext --inplace
