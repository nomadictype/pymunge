#!/usr/bin/env python

"""setup.py for pymunge.

Based on:
  https://github.com/pypa/sampleproject
  https://github.com/kennethreitz/setup.py
"""

from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from distutils.command.clean import clean
from codecs import open
import os
from os import path
import re
import subprocess
import sys

here = path.abspath(path.dirname(__file__))

# Detect current version
about = {}
with open(path.join(here, 'pymunge', '_version.py')) as f:
    exec(f.read(), about)

# Read description from readme
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()
    match = re.match(r'^(?:=+\n)?[^\n]+\n=+\n\s*(.*?)\.?\n{2,}(.*)', readme, re.DOTALL)
    if not match:
        raise AssertionError('Failed to parse description from README.rst')
    description = match.group(1).strip()
    long_description = match.group(2).strip()

class CleanCommand(clean):
    """Custom clean command to tidy up the project root."""
    def run(self):
        os.system('rm -vrf ./build ./dist ./deb_dist ./*.pyc ./pymunge-*.tar.gz ./pymunge-*.tgz ./*.egg-info')

class SdistCommand(sdist):
    """Custom sdist command to set owner/group to root for a files
    in the created tarball"""
    def run(self):
        super(SdistCommand, self).run()
        tar_chown_script = path.join(here, 'util', 'tar_chown.pl')
        for archive in self.get_archive_files():
            print('changing file ownerships in archive ' + archive)
            subprocess.call([tar_chown_script, archive])

if sys.version_info >= (3,4):
    install_requires = []
else:
    install_requires = ['enum34']

setup(
    name='pymunge',
    version=about['__version__'],
    description=description,
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
    install_requires=install_requires,
    cmdclass={
        'clean': CleanCommand,
        'sdist': SdistCommand,
    },
)
