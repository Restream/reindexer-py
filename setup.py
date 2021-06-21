import os
import sys
from multiprocessing import cpu_count

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig

if sys.version_info < (3, 6):
    raise RuntimeError('Require Python 3.6 or greater')

PACKAGE_NAME = 'pyreindexer'

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


class build_ext(build_ext_orig):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        cwd = os.path.abspath('')

        build_temp = os.path.abspath(self.build_temp)
        if not os.path.exists(build_temp):
            os.makedirs(build_temp)

        extension_dir = os.path.abspath(self.get_ext_fullpath(ext.name))
        if not os.path.exists(extension_dir):
            os.makedirs(extension_dir)

        os.chdir(build_temp)

        lib_dir = os.path.join(extension_dir, '..')
        source_dir = os.path.join(cwd, PACKAGE_NAME)

        self.spawn(['cmake', source_dir,
                    '-DCMAKE_BUILD_TYPE=Release',
                    '-DCMAKE_CXX_STANDARD=17',
                    '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + lib_dir])
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'])

        os.chdir(cwd)


setup(name=PACKAGE_NAME,
      version='0.2.1',
      description='A connector that allows to interact with Reindexer',
      url='https://github.com/Restream/pyreindexer',
      author='Igor Tulmentyev',
      author_email='igtulm@gmail.com',
      maintainer='Oleg Gerasimov',
      maintainer_email='ogerasimov@gmail.com',
      license='Apache License 2.0',
      packages=[PACKAGE_NAME],
      ext_modules=[CMakeExtension('rawpyreindexer')],
      cmdclass={'build_ext': build_ext},
      package_data={'pyreindexer': [
          'CMakeLists.txt',
          'lib/include/pyobjtools.h',
          'lib/include/pyobjtools.cc',
          'lib/include/queryresults_wrapper.h',
          'lib/src/rawpyreindexer.h',
          'lib/src/rawpyreindexer.cc',
          'lib/src/reindexerinterface.h',
          'lib/src/reindexerinterface.cc',
          'example/main.py',
          'tests/__init__.py',
          'tests/test_builtin.py',
          'tests/test_cproto.py'
      ]},
      test_suite='tests', install_requires=['envoy', 'delegator', 'pytest']
      )
