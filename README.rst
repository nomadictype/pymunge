===========
pymunge 0.1
===========

A Python interface to MUNGE.

MUNGE (MUNGE Uid 'N' Gid Emporium, https://dun.github.io/munge/)
is an authentication service for creating and validating credentials
designed to be highly scalable for use in an HPC cluster environment.

pymunge is a Python wrapper for the C API of MUNGE, called
libmunge.  pymunge provides functions and classes to create
and validate credentials with MUNGE, and to use and interact with
MUNGE contexts.

Official pymunge repository: https://github.com/nomadictype/pymunge

PyPI project page: https://pypi.python.org/pypi/pymunge


Install instructions
====================

Requirements:

* Python 3.4 or later (Python 2 is not supported.)
* MUNGE 0.5.x
* A munged daemon must be running on the same machine in order
  for pymunge to be able to create and validate credentials.

Make sure that all the above requirements are satisfied. Afterwards,
there are several possible ways to proceed:

* To install pymunge from PyPI, simply run::

    python3 -m pip install pymunge

* Alternatively, your OS distribution may include pymunge as a package,
  with a name such as pymunge, python3-pymunge, or python-pymunge.
* pymunge can also be used directly without installation - simply
  append the path containing the pymunge package to your
  PYTHONPATH environment variable.


Getting started / Tutorial
==========================

This quick tutorial describes how to use the pymunge API. If you want,
you can follow along in an interactive Python 3 session; simply copy
all the code preceded by `>>>`.

First of all, import the package:

>>> import pymunge

The simplest way to encode (= create) and decode (= validate) credentials
is to use the `pymunge.encode()` and `pymunge.decode()` functions.
For example:

>>> cred = pymunge.encode(b"some payload")
>>> cred
b'MUNGE:AwQDAA...'

The credential cred can now be sent to some other process (or passed
to the unmunge program) to decode it. For the purpose of this
tutorial, we simply decode it in the same process.

>>> payload, uid, gid, ctx = pymunge.decode(cred)
>>> payload
b'some payload'

`pymunge.decode()` returns 4 values: the payload that was encapsulated
within the credential, the UID/GID of the process that created the
credential, and a MUNGE context. This context can be examined to
obtain additional information about the credential:

>>> ctx.cipher_type
<CipherType.AES128: 4>
>>> ctx.encode_time
1514469923
>>> ctx.ttl
300
>>> ctx.uid_restriction
-1

(Also try running `help(ctx)` to see a list of all attributes
a context can have.)

It is possible to encode and decode within existing MUNGE
contexts. This is useful to customize the options used to
encode a credential:

>>> with pymunge.MungeContext() as ctx:
>>>     ctx.uid_restriction = 0  # allow only root to decode the credential
>>>     cred = ctx.encode(b"some other payload")

Similarly, `MungeContext.decode()` can be used to decode within an
existing context.

This concludes the basic tutorial. A collection of similar examples
is provided in the file `pymunge_example.py` distributed with pymunge.


Author
======

pymunge was written by nomadictype (https://github.com/nomadictype/).

License
-------

Copyright (C) 2017 nomadictype <nomadictype AT tutanota.com>

Like libmunge, pymunge is dual-licensed under GPL-3 and LGPL-3.
See LICENSE.txt for details.
