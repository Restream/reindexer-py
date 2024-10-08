import os
import sys

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig

if sys.version_info < (3, 6):
    raise RuntimeError('Require Python 3.6 or greater')

PACKAGE_NAME = 'pyreindexer'


def _c2(*names):
    return ' :: '.join(names)


class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


class BuildExt(build_ext_orig):
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
                    '-DCMAKE_BUILD_TYPE=RelWithDebInfo',
                    '-DCMAKE_CXX_STANDARD=17',
                    '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + lib_dir,
                    '-DCMAKE_OSX_DEPLOYMENT_TARGET=11'])
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'])

        os.chdir(cwd)


setup(name=PACKAGE_NAME,
      version='0.2.37',
      description='A connector that allows to interact with Reindexer',
      author='Igor Tulmentyev',
      author_email='igtulm@gmail.com',
      maintainer='Reindexer Team',
      maintainer_email='contactus@reindexer.io',
      url='https://github.com/Restream/reindexer-py',
      project_urls={
          'Documentation': 'https://reindexer.io/',
          'Releases': 'https://github.com/Restream/reindexer-py/releases',
          'Tracker': 'https://github.com/Restream/reindexer-py/issues',
      },
      long_description=open("README.md", encoding="utf-8").read(),
      long_description_content_type="text/markdown",
      license='Apache License 2.0',
      packages=[PACKAGE_NAME],
      ext_modules=[CMakeExtension('rawpyreindexer')],
      cmdclass={'build_ext': BuildExt},
      keywords=["reindexer", "in-memory-database", "database", "python", "connector"],
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
          'tests/conftest.py',
          'tests/test_data/constants.py',
          'tests/test_data/__init__.py',
          'tests/tests/test_sql.py',
          'tests/tests/test_index.py',
          'tests/tests/test_items.py',
          'tests/tests/test_database.py',
          'tests/tests/test_namespace.py',
          'tests/tests/test_metadata.py',
          'tests/tests/__init__.py',
          'tests/helpers/namespace.py',
          'tests/helpers/sql.py',
          'tests/helpers/items.py',
          'tests/helpers/index.py',
          'tests/helpers/metadata.py',
          'tests/helpers/log_helper.py',
          'tests/helpers/__init__.py',
          'tests/__init__.py'
      ]},
      python_requires=">=3.6,<3.13",
      test_suite='tests',
      install_requires=['envoy==0.0.3', 'delegator==0.0.3', 'pyhamcrest==2.0.2', 'pytest==6.2.5'],
      classifiers=[
          _c2('Development Status', '3 - Alpha'),
          _c2('Environment', 'Console'),
          _c2('Intended Audience', 'End Users/Desktop'),
          _c2('Intended Audience', 'Developers'),
          _c2('License', 'OSI Approved', 'Apache Software License'),
          _c2('Natural Language', 'Russian'),
          _c2('Operating System', 'MacOS'),
          _c2('Operating System', 'POSIX', 'Linux'),
          _c2('Operating System', 'Microsoft', 'Windows'),
          _c2('Programming Language', 'Python'),
          _c2('Programming Language', 'Python', '3.6'),
          _c2('Programming Language', 'Python', '3.7'),
          _c2('Programming Language', 'Python', '3.8'),
          _c2('Programming Language', 'Python', '3.9'),
          _c2('Programming Language', 'Python', '3.10'),
          _c2('Programming Language', 'Python', '3.11'),
          _c2('Programming Language', 'Python', '3.12'),
          _c2('Topic', 'Database'),
          _c2('Topic', 'Database', 'Database Engines/Servers'),
          _c2('Topic', 'Software Development'),
          _c2('Topic', 'Software Development', 'Libraries', 'Python Modules'),
      ],
      platforms=['ALT Linux', 'RED OS', 'Astra Linux'],
      )
