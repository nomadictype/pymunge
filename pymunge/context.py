#########################################################################
# Module pymunge.context - provides the MungeContext class
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

"""This module provides the MungeContext class and functions to encode
and decode credentials. The core of pymunge."""

from pymunge.error import MungeError, MungeErrorCode
from pymunge.enums import CipherType, MACType, ZipType
import pymunge.native
import ctypes
import socket
import struct

class MungeContext(object):
    """A MUNGE context. Encapsulates a collection of options used when
    creating a credential, or obtained from decoding a credential.

    A MungeContext can be used a context manager for a 'with' statement,
    closing the context when exiting the 'with' scope, e.g.:
    >>> with MungeContext() as ctx:
    >>>     do stuff with ctx
    """

    def __init__(self, ctx=None):
        """If ctx is None, create a new context (with all options set
        to their defaults initially).

        If ctx is not None, create a copy of ctx.
        """
        if ctx is not None:
            self.ctx = pymunge.native.munge_ctx_copy(ctx.ctx)
        else:
            self.ctx = pymunge.native.munge_ctx_create()

    def __del__(self):
        if hasattr(self, 'ctx'):
            self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Close this context, releasing any resources associated with it.
        Once a context is closed, it cannot be reopened, and it cannot be
        used to encode, decode, or to read or set options (in each case,
        a MungeError is raised). Calling close() on an already closed
        context has no effect."""
        if self.ctx is not None:
            pymunge.native.munge_ctx_destroy(self.ctx)
            self.ctx = None

    @property
    def closed(self):
        """True if this context is closed, False otherwise.
        This property cannot be explicitly set, instead use the
        close() method to close the context."""
        return self.ctx is None

    def encode(self, payload=None):
        """Create a MUNGE credential using the options defined in this
        context. Optionally, a payload (byte string) can be encapsulated
        as well.

        If successful, returns the credential (a byte string), otherwise
        raises a MungeError."""
        self._ensure_is_open()
        if isinstance(payload, bytes):
            return pymunge.native.munge_encode(self.ctx, payload, len(payload))
        elif payload is None:
            return pymunge.native.munge_encode(self.ctx, None, 0)
        else:
            raise TypeError('Payload must be bytes or None, got %s' %
                    type(payload).__name__)

    def decode(self, cred):
        """Validate a MUNGE credential. This context will be set to that
        used to encode the credential.

        If successful, returns (payload, uid, gid), where payload is the
        payload encapsulated in the credential, and uid, gid are the
        UID/GID of the process that created the credential.
        Otherwise a MungeError is raised. For certain errors
        (i.e. EMUNGE_CRED_EXPIRED, EMUNGE_CRED_REWOUND, EMUNGE_CRED_REPLAYED),
        the payload, uid and gid can still be obtained via the `result`
        property of the raised MungeError."""
        self._ensure_is_open()
        if isinstance(cred, bytes):
            return pymunge.native.munge_decode(cred, self.ctx)
        else:
            raise TypeError('Credential must be bytes, got %s' %
                    type(cred).__name__)

    @property
    def cipher_type(self):
        """Symmetric cipher type (a CipherType)."""
        return CipherType(self._get_option(pymunge.native.MUNGE_OPT_CIPHER_TYPE,
                ctypes.c_int))
    @cipher_type.setter
    def cipher_type(self, cipher_type):
        self._check_arg_type(cipher_type, "cipher_type", CipherType)
        self._set_option(pymunge.native.MUNGE_OPT_CIPHER_TYPE,
                ctypes.c_int, cipher_type.value)

    @property
    def mac_type(self):
        """Message authentication code type (a MACType)."""
        return MACType(self._get_option(pymunge.native.MUNGE_OPT_MAC_TYPE,
                ctypes.c_int))
    @mac_type.setter
    def mac_type(self, mac_type):
        self._check_arg_type(mac_type, "mac_type", MACType)
        self._set_option(pymunge.native.MUNGE_OPT_MAC_TYPE,
                ctypes.c_int, mac_type.value)

    @property
    def zip_type(self):
        """Compression type (a ZipType)."""
        return ZipType(self._get_option(pymunge.native.MUNGE_OPT_ZIP_TYPE,
                ctypes.c_int))
    @zip_type.setter
    def zip_type(self, zip_type):
        self._check_arg_type(zip_type, "zip_type", ZipType)
        self._set_option(pymunge.native.MUNGE_OPT_ZIP_TYPE,
                ctypes.c_int, zip_type.value)

    @property
    def realm(self):
        """Security realm (a str). Not currently supported."""
        r = self._get_option(pymunge.native.MUNGE_OPT_REALM,
                ctypes.c_char_p)
        if r is not None:
            return r.decode('utf-8')
        else:
            return None
    @realm.setter
    def realm(self, realm):
        if realm is not None:
            self._check_arg_type(realm, "realm", str)
            self._set_option(pymunge.native.MUNGE_OPT_REALM,
                    ctypes.c_char_p, realm.encode('utf-8'))
        else:
            self._set_option(pymunge.native.MUNGE_OPT_REALM,
                    ctypes.c_char_p, None)

    @property
    def ttl(self):
        """Time-to-live (in seconds). This value controls how long the
        credential is valid once it has been encoded.

        When encoding a credential, two special values can be used:
        * MUNGE_TTL_DEFAULT, which specifies the default according to the
        munged configuration. This is the default value of this property.
        * MUNGE_TTL_MAXIMUM, which specifies the maximum allowed by the
        munged configuration."""
        return self._get_option(pymunge.native.MUNGE_OPT_TTL, ctypes.c_int)
    @ttl.setter
    def ttl(self, ttl):
        self._check_arg_type(ttl, "ttl", int)
        self._set_option(pymunge.native.MUNGE_OPT_TTL,
                ctypes.c_int, ttl)

    @property
    def addr4(self):
        """The IPv4 address of the host where the credential was encoded,
        in dotted-quad notation (e.g. '127.0.0.1'). This property cannot be
        explicitly set."""
        ip = self._get_option(pymunge.native.MUNGE_OPT_ADDR4, ctypes.c_ulong)
        return socket.inet_ntoa(struct.pack('<L', ip))

    @property
    def encode_time(self):
        """The time (in seconds since the epoch) at which the credential
        was encoded. This property cannot be explicitly set."""
        return self._get_option(pymunge.native.MUNGE_OPT_ENCODE_TIME,
                pymunge.native.time_t)

    @property
    def decode_time(self):
        """The time (in seconds since the epoch) at which the credential
        was decoded. This property cannot be explicitly set."""
        return self._get_option(pymunge.native.MUNGE_OPT_DECODE_TIME,
                pymunge.native.time_t)

    @property
    def socket(self):
        """Path of the local domain socket for connecting with munged,
        a str."""
        return self._get_option(pymunge.native.MUNGE_OPT_SOCKET,
                ctypes.c_char_p).decode('utf-8')
    @socket.setter
    def socket(self, sock):
        self._check_arg_type(sock, "socket", str)
        self._set_option(pymunge.native.MUNGE_OPT_SOCKET,
                ctypes.c_char_p, sock.encode('utf-8'))

    @property
    def uid_restriction(self):
        """Numeric UID allowed to decode the credential. This value will be
        matched against the effective user ID of the process requesting the
        credential decode. Default is the special value UID_ANY, which
        means no UID restriction is set."""
        uid = self._get_option(pymunge.native.MUNGE_OPT_UID_RESTRICTION,
                pymunge.native.uid_t)
        if uid == pymunge.native.uid_t(pymunge.enums.UID_ANY).value:
            return pymunge.enums.UID_ANY
        else:
            return uid
    @uid_restriction.setter
    def uid_restriction(self, uid_restriction):
        self._check_arg_type(uid_restriction, "uid_restriction", int)
        self._set_option(pymunge.native.MUNGE_OPT_UID_RESTRICTION,
                pymunge.native.uid_t, uid_restriction)

    @property
    def gid_restriction(self):
        """Numeric GID allowed to decode the credential. This value will be
        matched against the effective group ID of the process requesting the
        credential decode. Default is the special value GID_ANY, which
        means no GID restriction is set."""
        gid = self._get_option(pymunge.native.MUNGE_OPT_GID_RESTRICTION,
                pymunge.native.gid_t)
        if gid == pymunge.native.gid_t(pymunge.enums.GID_ANY).value:
            return pymunge.enums.GID_ANY
        else:
            return gid
    @gid_restriction.setter
    def gid_restriction(self, gid_restriction):
        self._check_arg_type(gid_restriction, "gid_restriction", int)
        self._set_option(pymunge.native.MUNGE_OPT_GID_RESTRICTION,
                pymunge.native.gid_t, gid_restriction)

    def _ensure_is_open(self):
        if self.closed:
            raise MungeError(MungeErrorCode.EMUNGE_BAD_ARG, "Context is closed")

    def _check_arg_type(self, arg, argname, argtype):
        if not isinstance(arg, argtype):
            raise TypeError("%s must be of type %s" % (argname, argtype.__name__))

    def _get_option(self, option, option_type):
        self._ensure_is_open()
        val = option_type()
        result = pymunge.native.munge_ctx_get(self.ctx, option,
                        ctypes.byref(val))
        return val.value

    def _set_option(self, option, option_type, value):
        self._ensure_is_open()
        val = option_type(value)
        pymunge.native.munge_ctx_set(self.ctx, option, val)

def encode(payload=None):
    """Create a MUNGE credential using the default context.
    Optionally, a payload (byte string) can be encapsulated as well.

    If successful, returns the credential (a byte string), otherwise
    raises a MungeError."""
    with MungeContext() as ctx:
        return ctx.encode(payload)

def decode(cred):
    """Validate a MUNGE credential using the default context.

    If successful, returns (payload, uid, gid, ctx), where payload is the
    payload encapsulated in the credential, uid, gid are the
    UID/GID of the process that created the credential, and ctx is a
    MungeContext set to the one used to create the credential.

    If unsuccessful, a MungeError is raised. For certain errors
    (i.e. EMUNGE_CRED_EXPIRED, EMUNGE_CRED_REWOUND, EMUNGE_CRED_REPLAYED),
    the payload, uid and gid can still be obtained via the `result`
    property of the raised MungeError. Note that the context cannot
    be obtained from the MungeError; if you need it, manually create
    a MungeContext and use its decode() method."""
    ctx = MungeContext()
    payload, uid, gid = ctx.decode(cred)
    return payload, uid, gid, ctx

