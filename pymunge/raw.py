#########################################################################
# Module pymunge.raw - declarations of raw libmunge C functions
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

"""This module contains declarations of raw libmunge C functions
and constants.

Importing this module causes the libmunge shared library to be loaded.

Note that most function prototypes differ slightly from their C counterparts,
as follows:

* For all C functions that originally return an error code (`munge_err_t`),
  the corresponding Python wrapper instead checks the return value
  and raises a `MungeError` if the wrapped function returns anything
  other than `EMUNGE_SUCCESS`.

* Some functions originally return multiple values via pointer-based
  output arguments (e.g. uid and gid in `munge_decode`). The Python wrapper
  does not take these arguments and instead returns the multiple values
  as a tuple.
"""

import ctypes
import ctypes.util
import pymunge.error

#: Name of the libmunge shared object.
libmunge_filename = ctypes.util.find_library('mungey')

#: Handle to the loaded libmunge shared object (a `ctypes.CDLL` object).
libmunge = None
if libmunge_filename is not None:
    libmunge = ctypes.CDLL(libmunge_filename)
else:
    import warnings
    warnings.warn("libmunge not found. All calls to pymunge.raw will fail.")


### Helper functions ###

def load_function(name, restype, argtypes, paramflags, errcheck=None):
    """pymunge internal - helper to load functions from libmunge
    raises a `MungeError` if error_code is not `EMUNGE_SUCCESS`"""
    if libmunge is None:
        # Mock libmunge functions if the library was not found. This allows
        # readthedocs to build the sphinx docs for the package without
        # having libmunge installed.
        if argtypes == "*":
            args = "*args"
        else:
            argnames = [flag[1] for flag in paramflags if flag[0] & 2 == 0]
            args = ", ".join(argnames)
        def _raise(e):
            raise e
        return eval("lambda " + args + ": "
                "_raise(ImportError('libmunge not found'))")
    else:
        if argtypes == "*":
            function = getattr(libmunge, name)
            function.restype = restype
        else:
            prototype = ctypes.CFUNCTYPE(restype, *argtypes)
            function = prototype((name, libmunge), paramflags)
        if errcheck is not None:
            function.errcheck = errcheck
        return function

def check_and_raise(error_code, ctx, result):
    """pymunge internal - helper for error check functions;
    raises a `MungeError` if error_code is not `EMUNGE_SUCCESS`"""
    if error_code != pymunge.error.MungeErrorCode.EMUNGE_SUCCESS.value:
        if ctx is not None:
            message = munge_ctx_strerror(ctx).decode("utf-8")
        else:
            message = munge_strerror(error_code).decode("utf-8")
        raise pymunge.error.MungeError(error_code, message, result)

### Types ###

#: The `munge_ctx_t` C type, an opaque handle to a MUNGE context.
#: The low-level version of `MungeContext`.
munge_ctx_t = ctypes.c_void_p

#: The `munge_err_t` C enumeration type. Specifies a MUNGE error code.
#: The low-level version of `MungeErrorCode`.
munge_err_t = ctypes.c_int

#: The `munge_opt_t` C enumeration type. Specifies a MUNGE context option.
munge_opt_t = ctypes.c_int

#: The `munge_enum_t` C enumeration type. Specifies a MUNGE enumeration.
munge_enum_t = ctypes.c_int

#: The `uid_t` POSIX type. Specifies a numeric user ID.
uid_t = ctypes.c_uint

#: The `gid_t` POSIX type. Specifies a numeric group ID.
gid_t = ctypes.c_uint

#: The `time_t` C type. Specifies a timestamp.
time_t = ctypes.c_long


### Functions ###

def errcheck_munge_encode(error_code, func, arguments):
    """pymunge internal - error check function for munge_encode"""
    ctx = arguments[1]
    result = arguments[0].value
    check_and_raise(error_code, ctx, result)
    return result

munge_encode = load_function("munge_encode",
        munge_err_t, [ctypes.POINTER(ctypes.c_char_p),
            munge_ctx_t, ctypes.c_void_p, ctypes.c_int],
        ((2, "cred"), (1, "ctx", None), (1, "buf", None), (1, "len", 0)),
        errcheck_munge_encode)
"""
C prototype: `munge_err_t munge_encode(char **cred, munge_ctx_t ctx, const void *buf, int len);`

Note: when called from Python, returns `cred` instead of the `munge_err_t`.

Creates a credential contained in a base64 string.
A payload specified by a buffer `buf` (a byte string) of length `len`
can be encapsulated in as well.
If the munge context `ctx` is None, the default context will be used.
Returns the credential `cred` if the credential is successfully created;
otherwise, raises a `MungeError` containing the error code and message.
The error message may be more detailed if a `ctx` was specified.
"""

def errcheck_munge_decode(error_code, func, arguments):
    """pymunge internal - error check function for munge_decode"""
    ctx = arguments[1]
    buf = ctypes.string_at(arguments[2].value, arguments[3].value)
    result = (buf, arguments[4].value, arguments[5].value)
    check_and_raise(error_code, ctx, result)
    return result

munge_decode = load_function("munge_decode",
        munge_err_t, [ctypes.c_char_p, munge_ctx_t,
            ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(uid_t), ctypes.POINTER(gid_t)],
        ((1, "cred"), (1, "ctx", None), (2, "buf"), (2, "len"),
         (2, "uid"), (2, "gid")),
        errcheck_munge_decode)
"""
C prototype: `munge_err_t munge_decode(const char *cred, munge_ctx_t ctx, void **buf, int *len, uid_t *uid, gid_t *gid);`

Note: when called from Python, returns `(payload, uid, gid)` instead of the
`munge_err_t`, where `payload` is the contents of `buf` of length `len`.
Example usage:

>>> payload, uid, gid = munge_decode(cred, ctx)

Validates the credential `cred`.
If the munge context `ctx` is not None, it will be set to that used
to encode the credential.
If the credential is valid, returns the encapsulated payload byte string
`payload` as well as the numeric UID `uid` and GID `gid` of the process
that created the credential.
If the credential is not valid, raises a `MungeError` containing the
error code and message. The error message may be more detailed if a `ctx`
was specified. For certain errors (ie, `EMUNGE_CRED_EXPIRED`,
`EMUNGE_CRED_REWOUND`, `EMUNGE_CRED_REPLAYED`), the raised `MungeError` will
contain the result `(payload, uid, gid)` which would have been returned
if the credential were still valid.
"""

munge_strerror = load_function("munge_strerror",
        ctypes.c_char_p, [munge_err_t],
        ((1, "e"),))
"""
C prototype: `const char * munge_strerror(munge_err_t e);`

Returns a descriptive string describing the munge errno `e`.
"""

munge_ctx_create = load_function("munge_ctx_create",
        munge_ctx_t, [], ())
"""
C prototype: `munge_ctx_t munge_ctx_create(void);`

Creates and returns a new munge context or None on error.
Abandoning a context without calling `munge_ctx_destroy()` will result
in a memory leak.
"""

munge_ctx_copy = load_function("munge_ctx_copy",
        munge_ctx_t, [munge_ctx_t],
        ((1, "ctx"),))
"""
C prototype: `munge_ctx_t munge_ctx_copy(munge_ctx_t ctx);`

Copies the context `ctx`, returning a new munge context or None on error.
Abandoning a context without calling `munge_ctx_destroy()` will result
in a memory leak.
"""

munge_ctx_destroy = load_function("munge_ctx_destroy",
        None, [munge_ctx_t],
        ((1, "ctx"),))
"""
C prototype: `void munge_ctx_destroy(munge_ctx_t ctx);`

Destroys the context `ctx`.
"""

munge_ctx_strerror = load_function("munge_ctx_strerror",
        ctypes.c_char_p, [munge_ctx_t],
        ((1, "ctx"),))
"""
C prototype: `const char * munge_ctx_strerror(munge_ctx_t ctx);`

Returns a descriptive text string describing the munge error number
according to the context `ctx`, or None if no error condition exists.
This message may be more detailed than that returned by `munge_strerror()`.
"""

def errcheck_munge_ctx_getset(error_code, func, arguments):
    """pymunge internal - error check function for munge_ctx_get
    and munge_ctx_set"""
    ctx = arguments[0]
    check_and_raise(error_code, ctx, None)
    return arguments

munge_ctx_get = load_function("munge_ctx_get",
        munge_err_t, "*",
        (),
        errcheck_munge_ctx_getset)
"""
C prototype: `munge_err_t munge_ctx_get(munge_ctx_t ctx, munge_opt_t opt, ...);`

Note: when called from Python, returns nothing.

Gets the value for the option `opt` associated with the munge context `ctx`,
storing the result in the subsequent pointer argument. Refer to the
`munge_opt_t` enum comments for argument types. If the result is a string,
that string should not be freed or modified by the caller.
Raises a `MungeError` upon failure.
"""

munge_ctx_set = load_function("munge_ctx_set",
        munge_err_t, "*",
        (),
        errcheck_munge_ctx_getset)
"""
C prototype: `munge_err_t munge_ctx_set(munge_ctx_t ctx, munge_opt_t opt, ...);`

Note: when called from Python, returns nothing.

Sets the value for the option `opt` associated with the munge context `ctx`,
using the value of the subsequent argument. Refer to the `munge_opt_t`
enum comments for argument types. Raises a `MungeError` upon failure.
"""

munge_enum_is_valid = load_function("munge_enum_is_valid",
        ctypes.c_bool, [munge_enum_t, ctypes.c_int],
        ((1, "type"), (1, "val")))
"""
C prototype: `int munge_enum_is_valid(munge_enum_t type, int val);`

Note: when called from Python, the returned int is converted to a boolean.

Returns True if the given value `val` is a valid enumeration of the
specified type `type` in the software configuration as currently compiled;
otherwise returns False. Some enumerations correspond to options that can
only be enabled at compile-time.
"""

munge_enum_int_to_str = load_function("munge_enum_int_to_str",
        ctypes.c_char_p, [munge_enum_t, ctypes.c_int],
        ((1, "type"), (1, "val")))
"""
C prototype: `const char * munge_enum_int_to_str(munge_enum_t type, int val);`

Converts the munge enumeration `val` of the specified type `type`
into a text string. Returns the text string, or None on error.
"""

munge_enum_str_to_int = load_function("munge_enum_str_to_int",
        ctypes.c_int, [munge_enum_t, ctypes.c_char_p],
        ((1, "type"), (1, "str")))
"""
C prototype: `int munge_enum_str_to_int(munge_enum_t type, const char *str);`

Converts the case-insensitive byte string `str` into the corresponding
munge enumeration of the specified type `type`. Returns a munge
enumeration on success (>= 0), or -1 on error.
"""


### Enumerations (excluding those already present in pymunge.enums) ###

### MUNGE context options ###

MUNGE_OPT_CIPHER_TYPE       =  0    #: symmetric cipher type (int)
MUNGE_OPT_MAC_TYPE          =  1    #: message auth code type (int)
MUNGE_OPT_ZIP_TYPE          =  2    #: compression type (int)
MUNGE_OPT_REALM             =  3    #: security realm (str)
MUNGE_OPT_TTL               =  4    #: time-to-live (int)
MUNGE_OPT_ADDR4             =  5    #: src IPv4 addr (struct in_addr)
MUNGE_OPT_ENCODE_TIME       =  6    #: time when cred encoded (time_t)
MUNGE_OPT_DECODE_TIME       =  7    #: time when cred decoded (time_t)
MUNGE_OPT_SOCKET            =  8    #: socket for comm w/ daemon (str)
MUNGE_OPT_UID_RESTRICTION   =  9    #: UID able to decode cred (uid_t)
MUNGE_OPT_GID_RESTRICTION   = 10    #: GID able to decode cred (gid_t)

### MUNGE enum types for str/int conversions ###

MUNGE_ENUM_CIPHER           =  0    #: cipher enum type
MUNGE_ENUM_MAC              =  1    #: mac enum type
MUNGE_ENUM_ZIP              =  2    #: zip enum type


__all__ = [
        "munge_encode", "munge_decode", "munge_strerror",
        "munge_ctx_create", "munge_ctx_copy", "munge_ctx_destroy",
        "munge_ctx_strerror", "munge_ctx_get", "munge_ctx_set",
        "munge_enum_is_valid", "munge_enum_int_to_str", "munge_enum_str_to_int",

        "libmunge_filename", "libmunge",

        "uid_t", "gid_t", "time_t", "munge_ctx_t", "munge_err_t",

        "munge_opt_t",
        "MUNGE_OPT_CIPHER_TYPE", "MUNGE_OPT_MAC_TYPE", "MUNGE_OPT_ZIP_TYPE",
        "MUNGE_OPT_REALM", "MUNGE_OPT_TTL", "MUNGE_OPT_ADDR4",
        "MUNGE_OPT_ENCODE_TIME", "MUNGE_OPT_DECODE_TIME", "MUNGE_OPT_SOCKET",
        "MUNGE_OPT_UID_RESTRICTION", "MUNGE_OPT_GID_RESTRICTION",

        "munge_enum_t",
        "MUNGE_ENUM_CIPHER", "MUNGE_ENUM_MAC", "MUNGE_ENUM_ZIP",
]
