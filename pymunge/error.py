#########################################################################
# Module pymunge.error - MUNGE exceptions and error codes
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

"""MUNGE exceptions and error codes"""

import enum

class MungeErrorCode(enum.Enum):
    """MUNGE error codes."""
    EMUNGE_SUCCESS              =  0
    EMUNGE_SNAFU                =  1
    EMUNGE_BAD_ARG              =  2
    EMUNGE_BAD_LENGTH           =  3
    EMUNGE_OVERFLOW             =  4
    EMUNGE_NO_MEMORY            =  5
    EMUNGE_SOCKET               =  6
    EMUNGE_TIMEOUT              =  7
    EMUNGE_BAD_CRED             =  8
    EMUNGE_BAD_VERSION          =  9
    EMUNGE_BAD_CIPHER           = 10
    EMUNGE_BAD_MAC              = 11
    EMUNGE_BAD_ZIP              = 12
    EMUNGE_BAD_REALM            = 13
    EMUNGE_CRED_INVALID         = 14
    EMUNGE_CRED_EXPIRED         = 15
    EMUNGE_CRED_REWOUND         = 16
    EMUNGE_CRED_REPLAYED        = 17
    EMUNGE_CRED_UNAUTHORIZED    = 18

class MungeError(Exception):
    def __init__(self, code, message, result = None):
        """Generic MUNGE exception. Generally raised when an underlying
        libmunge function returns an error code, or in a few cases
        when a pymunge wrapper detects an invalid argument.

        MungeError instances have the following attributes:
        * code: The error code (a MungeErrorCode, which is NOT an integer).
          To retrieve the raw error case as an integer, use `code.value`.
        * message: The message string from libmunge. This is only the
          raw message without the exception type or the error code.
        * result: Partial result, in most cases None.
          If a decode fails with one of certain errors (i.e.
          EMUNGE_CRED_EXPIRED, EMUNGE_CRED_REWOUND, EMUNGE_CRED_REPLAYED),
          result is a 3-tuple (payload, uid, gid) containing the results
          that would have been returned by the decode function or method.
        """
        if not isinstance(code, MungeErrorCode):
            code = MungeErrorCode(code)
        super(MungeError, self).__init__("%s (error code %d: %s)" %
                (message, code.value, code.name))
        self.code = code
        self.message = message
        self.result = result
