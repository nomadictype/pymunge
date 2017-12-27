#!/usr/bin/env python3

import munge
from datetime import datetime

# Encoding a credential

with munge.MungeContext() as ctx:
    ctx.cipher_type = munge.CipherType.AES256
    ctx.mac_type = munge.MACType.SHA256
    cred = ctx.encode(b"Meet tomorrow 8:45")

print("Created credential: %r" % cred)
print()

# Decoding a credential

with munge.MungeContext() as ctx:
    payload, uid, gid = ctx.decode(cred)
    print("Successfully decoded credential")
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

print()

# Example of exception handling
# Decoding the credential again results in a 'credential replayed' error

with munge.MungeContext() as ctx:
    payload, uid, gid = ctx.decode(cred)
    # ^ results in:
    # munge.error.MungeError: Replayed credential (error code 17: EMUNGE_CRED_REPLAYED)
    # If desired, the decoding result can be obtained from the 'result'
    # property of the MungeError.
