import os
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as build_ext_orig


if sys.version_info < (3, 8):
    raise RuntimeError('Require Python 3.8 or greater')

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
        os.makedirs(os.path.abspath(self.build_temp), exist_ok=True)

        cwd = os.path.abspath('')
        extension_dir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        self.spawn(['cmake',
                    os.path.join(cwd, PACKAGE_NAME),
                    f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extension_dir}',
                    '-DCMAKE_BUILD_TYPE=Release',
                    '-DCMAKE_CXX_STANDARD=20',
                    f'-DCMAKE_OSX_DEPLOYMENT_TARGET={os.getenv("MACOSX_DEPLOYMENT_TARGET", "14")}'])

        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'])
        os.chdir(cwd)


with open('README.md', 'r', encoding='utf-8') as file:
    LONG_DESCRIPTION = file.read()

setup(name=PACKAGE_NAME,
      version='0.5.100000',
      description='A connector that allows to interact with Reindexer. Reindexer static library or reindexer-dev package must be installed',
      author='Igor Tulmentyev',
      author_email='contactus@reindexer.io',
      maintainer='Reindexer Team',
      maintainer_email='contactus@reindexer.io',
      url='https://github.com/Restream/reindexer',
      download_url='https://github.com/Restream/reindexer-py',
      project_urls={
          'Documentation': 'https://reindexer.io/',
          # 'Releases': 'https://github.com/Restream/reindexer-py/releases',
          # 'Tracker': 'https://github.com/Restream/reindexer-py/issues',
          'Telegram chat': 'https://t.me/reindexer',
      },
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      license='Apache License 2.0',
      packages=[PACKAGE_NAME],
      ext_modules=[CMakeExtension('rawpyreindexer')],
      cmdclass={'build_ext': BuildExt},
      keywords=['reindexer', 'reindexer-py', 'in-memory-database', 'database', 'python', 'connector'],
      package_data={'pyreindexer': [
          'CMakeLists.txt',
          'lib/**/*',
          'example/main.py',
          'tests/**/*.py'
      ]},
      python_requires='>=3.8',
      install_requires=['PyHamcrest==2.0.2', 'pytest>=6.2.5', 'requests>=2.26.0'],
      classifiers=[
          _c2('Development Status', '4 - Beta'),
          _c2('Environment', 'Console'),
          _c2('Intended Audience', 'End Users/Desktop'),
          _c2('Intended Audience', 'Developers'),
          _c2('Natural Language', 'Russian'),
          _c2('Operating System', 'MacOS'),
          _c2('Operating System', 'POSIX', 'Linux'),
          _c2('Programming Language', 'Python'),
          _c2('Programming Language', 'Python', '3', 'Only'),
          _c2('Programming Language', 'Python', '3.8'),
          _c2('Programming Language', 'Python', '3.9'),
          _c2('Programming Language', 'Python', '3.10'),
          _c2('Programming Language', 'Python', '3.11'),
          _c2('Programming Language', 'Python', '3.12'),
          _c2('Programming Language', 'Python', '3.13'),
          _c2('Programming Language', 'Python', 'Implementation'),
          _c2('Programming Language', 'Python', 'Implementation', 'CPython'),
          _c2('Programming Language', 'Python', 'Implementation', 'PyPy'),
          _c2('Topic', 'Database'),
          _c2('Topic', 'Database', 'Database Engines/Servers'),
          _c2('Topic', 'Software Development'),
          _c2('Topic', 'Software Development', 'Libraries'),
          _c2('Topic', 'Software Development', 'Libraries', 'Python Modules'),
          _c2('Topic', 'Software Development', 'Libraries', 'Application Frameworks'),
      ],
      platforms=['Ubuntu', 'Debian', 'ALT Linux', 'RED OS', 'Astra Linux', 'MacOS'],
      )
