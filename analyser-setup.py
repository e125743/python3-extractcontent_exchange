from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext_module = Extension(
    "analyser",
    ["analyser.pyx"],
    extra_compile_args=['-fopenmp'],
    extra_link_args=['-fopenmp'],
)

setup(
    name = 'Hello world app',
    cmdclass = {'build_analyser': build_ext},
    ext_modules = cythonize([ext_module]),
)
