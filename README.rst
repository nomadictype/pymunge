=============
pymunge 0.1.3
=============

A Python interface to MUNGE.

pymunge is a Python wrapper for the C API of MUNGE, called
libmunge.  pymunge provides functions and classes to create
and validate credentials with MUNGE, and to use and interact with
MUNGE contexts.

MUNGE (MUNGE Uid 'N' Gid Emporium, https://dun.github.io/munge/)
is an authentication service for creating and validating credentials
designed to be highly scalable for use in an HPC cluster environment.

Official pymunge repository: https://github.com/nomadictype/pymunge

PyPI project page: https://pypi.python.org/pypi/pymunge

API reference: https://pymunge.readthedocs.io/en/latest/


Install instructions
====================

Requirements:

* Python 3.4 or later (or Python 2.7 with the 'enum34' package).
* MUNGE 0.5.x or later.
* A munged daemon must be running on the same machine in order
  for pymunge to be able to create and validate credentials.

Make sure that all the above requirements are satisfied. Afterwards,
there are several possible ways to proceed:

* To install pymunge from PyPI, run the following command (preferably
  in a virtualenv)::

    python3 -m pip install pymunge

* Alternatively, your OS distribution may include pymunge as a package,
  with a name such as pymunge, python3-pymunge, or python-pymunge.

* pymunge can also be used directly without installation. Just ensure
  that Python can find the pymunge package (for example by appending
  the parent directory of the pymunge package to the PYTHONPATH
  environment variable).


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

The credential `cred` can now be sent to some other process to decode it
(via a socket or some other IPC mechanism) -- this is the responsibility
of the program which uses pymunge, pymunge does not provide any functions
to do this! For testing purposes, you can also pipe the credential into
the `unmunge` program by hand. To keep this tutorial simple, let us
decode the credential directly in the same process:

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

Copyright (C) 2017-2018 nomadictype <nomadictype AT tutanota.com>

Like libmunge, pymunge is dual-licensed under GPL-3 and LGPL-3.
See LICENSE.txt for details.



.. image:: https://img.shields.io/github/release/nomadictype/pymunge.svg
  :target: https://github.com/nomadictype/pymunge/releases

.. image:: https://img.shields.io/pypi/v/pymunge.svg
  :target: https://pypi.python.org/pypi/pymunge

.. image:: https://travis-ci.org/nomadictype/pymunge.svg?branch=master
  :target: https://travis-ci.org/nomadictype/pymunge

.. image:: https://img.shields.io/coveralls/github/nomadictype/pymunge.svg
  :target: https://coveralls.io/github/nomadictype/pymunge

.. image:: https://readthedocs.org/projects/pymunge/badge/?version=latest
  :target: https://pymunge.readthedocs.io/en/latest/?badge=latest

