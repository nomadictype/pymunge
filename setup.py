"""setup.py for pymunge.

Based on:
  https://github.com/pypa/sampleproject
  https://github.com/kennethreitz/setup.py
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Detect current version
about = {}
with open(path.join(here, 'pymunge', '_version.py')) as f:
    exec(f.read(), about)

# Read long description from readme
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pymunge',
    version=about['__version__'],
    description='A Python interface to MUNGE',
    long_description=long_description,
    url='https://github.com/nomadictype/pymunge',
    author='nomadictype',
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='munge libmunge hpc cluster authentication credentials',
    packages=['pymunge'],
    install_requires=[],
)
