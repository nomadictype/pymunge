#########################################################################
# Module pymunge.enums - MUNGE enumerations
# Copyright (C) 2017-2018 nomadictype <nomadictype AT tutanota.com>
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

"""MUNGE enumerations"""

import enum

class CipherType(enum.Enum):
    """MUNGE symmetric cipher types"""
    Disabled   =  0    #: encryption disabled
    Default    =  1    #: default cipher specified by daemon
    Blowfish   =  2    #: Blowfish CBC with 64b-block/128b-key
    CAST5      =  3    #: CAST5 CBC with 64b-block/128b-key
    AES128     =  4    #: AES CBC with 128b-block/128b-key
    AES256     =  5    #: AES CBC with 128b-block/256b-key

class MACType(enum.Enum):
    """MUNGE message authentication code types"""
    Disabled   =  0    #: MAC disabled -- invalid, btw
    Default    =  1    #: default MAC specified by daemon
    MD5        =  2    #: MD5 with 128b-digest
    SHA1       =  3    #: SHA-1 with 160b-digest
    RIPEMD160  =  4    #: RIPEMD-160 with 160b-digest
    SHA256     =  5    #: SHA-256 with 256b-digest
    SHA512     =  6    #: SHA-512 with 512b-digest

class ZipType(enum.Enum):
    """MUNGE compression types"""
    Disabled   =  0    #: compression disabled
    Default    =  1    #: default zip specified by daemon
    bzlib      =  2    #: bzip2 by Julian Seward
    zlib       =  3    #: zlib "deflate" by Gailly & Adler

TTL_MAXIMUM    = -1    #: Use the maximum TTL allowed by the daemon.
TTL_DEFAULT    =  0    #: Use the default TTL specified by the daemon.
UID_ANY        = -1    #: Do not restrict decode to a specific UID.
GID_ANY        = -1    #: Do not restrict decode to a specific GID.
