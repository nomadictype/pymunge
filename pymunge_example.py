#!/usr/bin/env python
#########################################################################
# pymunge_example.py - a set of simple usage examples for pymunge
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

import pymunge
from datetime import datetime

######

print(">>> Basic usage: Encoding and decoding credentials")

cred = pymunge.encode(b"Meet at the bridge")
print("Created credential: %r" % cred)
payload, uid, gid, ctx = pymunge.decode(cred)
print("Successfully decoded credential")
print("Payload: %r" % payload)

print("")

######

print(">>> Encoding a credential using a context")

with pymunge.MungeContext() as ctx:
    ctx.cipher_type = pymunge.CipherType.AES256
    ctx.mac_type = pymunge.MACType.SHA256
    cred2 = ctx.encode(b"Meet tomorrow 8:45")

print("Created credential 2: %r" % cred2)
print("")

######

print(">>> Decoding a credential using a context")

with pymunge.MungeContext() as ctx:
    payload, uid, gid = ctx.decode(cred2)
    print("Successfully decoded credential 2")
    print("Payload:          %r" % payload)
    print("UID:              %d" % uid)
    print("GID:              %d" % gid)
    print("Cipher type:      %r" % ctx.cipher_type)
    print("MAC type:         %r" % ctx.mac_type)
    print("ZIP type:         %r" % ctx.zip_type)
    print("Realm:            %r" % ctx.realm)
    print("TTL:              %d" % ctx.ttl)
    print("IPv4 address:     %r" % ctx.addr4)
    print("Encode time:      %s" % datetime.fromtimestamp(ctx.encode_time))
    print("Decode time:      %s" % datetime.fromtimestamp(ctx.decode_time))
    print("Socket:           %r" % ctx.socket)
    print("UID restriction:  %d" % ctx.uid_restriction)
    print("GID restriction:  %d" % ctx.gid_restriction)

print("")

######

print(">>> Exception handling example")
print("Re-decoding a credential should result in a 'replayed credential' error")

with pymunge.MungeContext() as ctx:
    try:
        payload, uid, gid = ctx.decode(cred2)
    except pymunge.MungeError as err:
        print("Caught MungeError: " + str(err))
        if err.code == pymunge.MungeErrorCode.EMUNGE_CRED_REPLAYED:
            print("It is possible to recover the decode result " +
                    "from a replayed credential:")
            payload, uid, gid = err.result
            print("  Payload:      %r" % payload)
            print("  UID:          %d" % uid)
            print("  GID:          %d" % gid)
            print("  Cipher type:  %r" % ctx.cipher_type)
            print("  (etc.)")

