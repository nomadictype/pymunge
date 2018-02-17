#########################################################################
# Module pymunge.native - declarations of native libmunge C functions
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

"""Declarations of native libmunge C functions and constants"""

import ctypes
import ctypes.util
import pymunge.error
import sys

libmunge_filename = ctypes.util.find_library('munge')
libmunge = ctypes.CDLL(libmunge_filename)

munge_opt_t = ctypes.c_int
munge_err_t = ctypes.c_int
munge_ctx_t = ctypes.c_void_p
munge_enum_t = ctypes.c_int
uid_t = ctypes.c_uint
gid_t = ctypes.c_uint
time_t = ctypes.c_long

def check_and_raise(error_code, ctx, result):
    """pymunge internal - helper for error check functions;
    raises a MungeError if error_code is not EMUNGE_SUCCESS"""
    if error_code != pymunge.error.MungeErrorCode.EMUNGE_SUCCESS.value:
        if ctx is not None:
            message = munge_ctx_strerror(ctx).decode("utf-8")
        else:
            message = munge_strerror(error_code).decode("utf-8")
        raise pymunge.error.MungeError(error_code, message, result)

# MUNGE context options
MUNGE_OPT_CIPHER_TYPE       =  0    # symmetric cipher type (int)
MUNGE_OPT_MAC_TYPE          =  1    # message auth code type (int)
MUNGE_OPT_ZIP_TYPE          =  2    # compression type (int)
MUNGE_OPT_REALM             =  3    # security realm (str)
MUNGE_OPT_TTL               =  4    # time-to-live (int)
MUNGE_OPT_ADDR4             =  5    # src IPv4 addr (struct in_addr)
MUNGE_OPT_ENCODE_TIME       =  6    # time when cred encoded (time_t)
MUNGE_OPT_DECODE_TIME       =  7    # time when cred decoded (time_t)
MUNGE_OPT_SOCKET            =  8    # socket for comm w/ daemon (str)
MUNGE_OPT_UID_RESTRICTION   =  9    # UID able to decode cred (uid_t)
MUNGE_OPT_GID_RESTRICTION   = 10    # GID able to decode cred (gid_t)

# MUNGE enum types for str/int conversions
MUNGE_ENUM_CIPHER           =  0    # cipher enum type
MUNGE_ENUM_MAC              =  1    # mac enum type
MUNGE_ENUM_ZIP              =  2    # zip enum type

#
#    cred = pymunge.native.munge_encode(ctx, buf, len)
#
# Creates a credential contained in a base64 string.
# A payload specified by a buffer [buf] (a byte string) of length [len]
# can be encapsulated in as well.
# If the munge context [ctx] is None, the default context will be used.
# Returns the credential [cred] if the credential is successfully created;
# o/w, raises a MungeError containing the error code and message.
# The error message may be more detailed if a [ctx] was specified.
#
_prototype = ctypes.CFUNCTYPE(munge_err_t,
        ctypes.POINTER(ctypes.c_char_p),
        munge_ctx_t, ctypes.c_void_p, ctypes.c_int)
munge_encode = _prototype(("munge_encode", libmunge),
        ((2, "cred"), (1, "ctx", None), (1, "buf", None), (1, "len", 0)))
def errcheck_munge_encode(error_code, func, arguments):
    """pymunge internal - error check function for munge_encode"""
    ctx = arguments[1]
    result = arguments[0].value
    check_and_raise(error_code, ctx, result)
    return result
munge_encode.errcheck = errcheck_munge_encode

#
#    payload, uid, gid = pymunge.native.munge_decode(cred, ctx)
#
# Validates the credential [cred].
# If the munge context [ctx] is not None, it will be set to that used
# to encode the credential.
# If the credential is valid, returns the encapsulated payload byte string
# [payload] as well as the numeric UID [uid] and GID [gid] of the process
# that created the credential.
# If the credential is not valid, raises a MungeError containing the
# error code and message. The error message may be more detailed if a [ctx]
# was specified. For certain errors (ie, EMUNGE_CRED_EXPIRED,
# EMUNGE_CRED_REWOUND, EMUNGE_CRED_REPLAYED), the raised MungeError will
# contain the result (payload, uid, gid) which would have been returned
# if the credential were still valid.
#
_prototype = ctypes.CFUNCTYPE(munge_err_t,
        ctypes.c_char_p, munge_ctx_t,
        ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(uid_t), ctypes.POINTER(gid_t))
munge_decode = _prototype(("munge_decode", libmunge),
        ((1, "cred"), (1, "ctx", None), (2, "buf"), (2, "len"),
         (2, "uid"), (2, "gid")))
def errcheck_munge_decode(error_code, func, arguments):
    """pymunge internal - error check function for munge_decode"""
    ctx = arguments[1]
    buf = ctypes.string_at(arguments[2].value, arguments[3].value)
    result = (buf, arguments[4].value, arguments[5].value)
    check_and_raise(error_code, ctx, result)
    return result
munge_decode.errcheck = errcheck_munge_decode

#
#    message = pymunge.native.munge_strerror(e)
#
# Returns a descriptive string describing the munge errno [e].
#
_prototype = ctypes.CFUNCTYPE(ctypes.c_char_p, munge_err_t)
munge_strerror = _prototype(("munge_strerror", libmunge),
        ((1, "e"),))

#
#    ctx = pymunge.native.munge_ctx_create()
#
# Creates and returns a new munge context or None on error.
# Abandoning a context without calling munge_ctx_destroy() will result
# in a memory leak.
#
_prototype = ctypes.CFUNCTYPE(munge_ctx_t)
munge_ctx_create = _prototype(("munge_ctx_create", libmunge))

#
#    ctx = pymunge.native.munge_ctx_copy(ctx)
#
# Copies the context [ctx], returning a new munge context or None on error.
# Abandoning a context without calling munge_ctx_destroy() will result
# in a memory leak.
#
_prototype = ctypes.CFUNCTYPE(munge_ctx_t, munge_ctx_t)
munge_ctx_copy = _prototype(("munge_ctx_copy", libmunge),
        ((1, "ctx"),))

#
#    pymunge.native.munge_ctx_destroy(ctx)
#
# Destroys the context [ctx].
#
_prototype = ctypes.CFUNCTYPE(None, munge_ctx_t)
munge_ctx_destroy = _prototype(("munge_ctx_destroy", libmunge),
        ((1, "ctx"),))

#
#    message = pymunge.native.munge_ctx_strerror(ctx)
#
# Returns a descriptive text string describing the munge error number
# according to the context [ctx], or None if no error condition exists.
# This message may be more detailed than that returned by munge_strerror().
#
_prototype = ctypes.CFUNCTYPE(ctypes.c_char_p, munge_ctx_t)
munge_ctx_strerror = _prototype(("munge_ctx_strerror", libmunge),
        ((1, "ctx"),))

#
#    pymunge.native.munge_ctx_get(ctx, opt, ...)
#
# Gets the value for the option [opt] (of munge_opt_t) associated with the
# munge context [ctx], storing the result in the subsequent pointer
# argument.  Refer to the munge_opt_t enum comments for argument types.
# If the result is a string, that string should not be freed or modified
# by the caller.
# Raises a MungeError upon failure.
#
munge_ctx_get = libmunge.munge_ctx_get
munge_ctx_get.restype = munge_err_t
def errcheck_munge_ctx_getset(error_code, func, arguments):
    """pymunge internal - error check function for munge_ctx_get
    and munge_ctx_set"""
    ctx = arguments[0]
    check_and_raise(error_code, ctx, None)
    return arguments
munge_ctx_get.errcheck = errcheck_munge_ctx_getset

#
#    pymunge.native.munge_ctx_set(ctx, opt, ...)
#
# Sets the value for the option [opt] (of munge_opt_t) associated with the
# munge context [ctx], using the value of the subsequent argument.
# Refer to the munge_opt_t enum comments for argument types.
# Raises a MungeError upon failure.
#
munge_ctx_set = libmunge.munge_ctx_set
munge_ctx_set.restype = munge_err_t
munge_ctx_set.errcheck = errcheck_munge_ctx_getset

#
#    is_valid = pymunge.native.munge_enum_is_valid(type, val)
#
# Returns True if the given value [val] is a valid enumeration of
# the specified type [type] in the software configuration as currently
# compiled; o/w, returns False.
# Some enumerations corresond to options that can only be enabled at
# compile-time.
#
_prototype = ctypes.CFUNCTYPE(ctypes.c_bool, munge_enum_t, ctypes.c_int)
munge_enum_is_valid = _prototype(("munge_enum_is_valid", libmunge),
        ((1, "type"), (1, "val")))

#
#    s = pymunge.native.munge_enum_int_to_str(type, val)
#
# Converts the munge enumeration [val] of the specified type [type]
# into a text string. Returns the text string, or None on error.
#
_prototype = ctypes.CFUNCTYPE(ctypes.c_char_p, munge_enum_t, ctypes.c_int)
munge_enum_int_to_str = _prototype(("munge_enum_int_to_str", libmunge),
        ((1, "type"), (1, "val")))

#
#    num = pymunge.native.munge_enum_str_to_int(type, str)
#
# Converts the case-insensitive byte string [str] into the corresponding
# munge enumeration of the specified type [type].
# Returns a munge enumeration on success (>=0), or -1 on error.
#
_prototype = ctypes.CFUNCTYPE(ctypes.c_int, munge_enum_t, ctypes.c_char_p)
munge_enum_str_to_int = _prototype(("munge_enum_str_to_int", libmunge),
        ((1, "type"), (1, "str")))

del _prototype
