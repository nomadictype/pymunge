"""A Python interface to libmunge, the MUNGE API.

MUNGE (MUNGE Uid 'N' Gid Emporium) is an authentication service for creating
and validating credentials."""

import munge.context
from munge.context import MungeContext, encode, decode

import munge.error
from munge.error import MungeError, MungeErrorCode

import munge.enums
from munge.enums import CipherType, MACType, ZipType, TTL_MAXIMUM, TTL_DEFAULT, UID_ANY, GID_ANY

import munge.native

__all__ = ['MungeContext', 'encode', 'decode',
        'MungeError', 'MungeErrorCode',
        'CipherType', 'MACType', 'ZipType',
        'TTL_MAXIMUM', 'TTL_DEFAULT', 'UID_ANY', 'GID_ANY']

