from os import path
from re import search
from setuptools import setup

PACKAGE_NAME = "puni"
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, PACKAGE_NAME, 'version.py'),
          encoding='utf-8') as fp:
    VERSION = search("__version__ = '([^']+)'", fp.read()).group(1)

setup(name=PACKAGE_NAME,
      version=VERSION,
      description='Python UserNotes Interface for reddit',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Utilities',
      ],
      url='http://github.com/teaearlgraycold/puni',
      author='teaearlgraycold',
      license='GPLv3',
      packages=[PACKAGE_NAME],
      install_requires=[
          'praw >=3.5.0, <4.0',
      ],tests_require = [
          'nose',
      ],
      test_suite="nose.collector",
      zip_safe=False
)
