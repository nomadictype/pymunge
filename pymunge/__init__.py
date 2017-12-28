#########################################################################
# __init__.py of package pymunge
# Copyright (C) 2017 nomadictype <nomadictype AT tutanota.com>
#
# pymunge is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  Additionally, you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# pymunge is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# and GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# and GNU Lesser General Public License along with pymunge.  If not, see
# <http://www.gnu.org/licenses/>.
#########################################################################

"""A Python interface to MUNGE.

pymunge is a Python wrapper for the C API of MUNGE, called
libmunge.  pymunge provides functions and classes to encode
and decode credentials with MUNGE, and to use and interact with
MUNGE contexts.  A working installation of MUNGE (a running
munged daemon, in particular) is required to encode and decode
credentials with pymunge.

Description of MUNGE from the MUNGE readme:
MUNGE (MUNGE Uid 'N' Gid Emporium) is an authentication service
for creating and validating credentials.  It is designed to be
highly scalable for use in an HPC cluster environment.  It allows
a process to authenticate the UID and GID of another local or
remote process within a group of hosts having common users and
groups.  These hosts form a security realm that is defined by a
shared cryptographic key.  Clients within this security realm can
create and validate credentials without the use of root privileges,
reserved ports, or platform-specific methods.

pymunge links:
  PyPI project page:    <https://pypi.python.org/pypi/pymunge>
  Official repository:  <https://github.com/nomadictype/pymunge>

MUNGE links:
  Project homepage:     <https://dun.github.io/munge/>
  Official repository:  <https://github.com/dun/munge>
"""

from pymunge._version import __version__

import pymunge.context
from pymunge.context import MungeContext, encode, decode

import pymunge.error
from pymunge.error import MungeError, MungeErrorCode

import pymunge.enums
from pymunge.enums import CipherType, MACType, ZipType, \
        TTL_MAXIMUM, TTL_DEFAULT, UID_ANY, GID_ANY

import pymunge.native

__all__ = ['MungeContext', 'encode', 'decode',
        'MungeError', 'MungeErrorCode',
        'CipherType', 'MACType', 'ZipType',
        'TTL_MAXIMUM', 'TTL_DEFAULT', 'UID_ANY', 'GID_ANY']

