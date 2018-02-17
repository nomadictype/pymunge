API reference
=============

.. module:: pymunge

Basic encoding and decoding
---------------------------

.. autofunction:: pymunge.encode

.. autofunction:: pymunge.decode

MUNGE contexts
----------------------------------------

.. autoclass:: pymunge.MungeContext
     :no-show-inheritance:

Enumerations and constants
--------------------------

.. autoclass:: pymunge.CipherType

.. autoclass:: pymunge.MACType

.. autoclass:: pymunge.ZipType

.. data:: pymunge.TTL_MAXIMUM

     Use the maximum TTL allowed by the daemon.

.. data:: pymunge.TTL_DEFAULT

     Use the default TTL specified by the daemon.

.. data:: pymunge.UID_ANY

     Do not restrict decode to a specific UID.

.. data:: pymunge.GID_ANY

     Do not restrict decode to a specific GID.

Exceptions
----------

.. autoclass:: pymunge.MungeError

.. autoclass:: pymunge.MungeErrorCode

Low-level API
-------------

.. toctree::
     :caption: Low-level API
     :hidden:

     api-lowlevel

The `pymunge.raw` module provides access to the low-level C API of libmunge.
See the :doc:`module documentation <api-lowlevel>`.

