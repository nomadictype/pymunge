#########################################################################
# Tests for module pymunge.context
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

from pymunge.context import MungeContext, encode, decode
from pymunge.enums import CipherType, MACType, ZipType, \
    TTL_DEFAULT, UID_ANY, GID_ANY
from pymunge.error import MungeError, MungeErrorCode
import pymunge.raw

import pytest
import os
import time

class MockContextDestroy(object):
    """Mocks/monkeypatches pymunge.raw.munge_ctx_destroy and counts
    how often it has been called"""

    def __init__(self, monkeypatch):
        self.history = []
        self.mocked_function = pymunge.raw.munge_ctx_destroy
        monkeypatch.setattr(pymunge.raw, 'munge_ctx_destroy', self)

    def __call__(self, ctx):
        self.history.append(ctx)
        self.mocked_function(ctx)

def test_construct_context():
    ctx1 = MungeContext()
    assert isinstance(ctx1, MungeContext)
    assert ctx1.ctx is not None

    ctx2 = MungeContext(None)
    assert isinstance(ctx2, MungeContext)
    assert ctx2.ctx is not None
    assert ctx2.ctx != ctx1.ctx

    ctx3 = MungeContext(ctx2)
    assert isinstance(ctx3, MungeContext)
    assert ctx3.ctx is not None
    assert ctx3.ctx != ctx2.ctx
    assert ctx3.ctx != ctx1.ctx

def test_close_context(monkeypatch):
    mock_ctx_destroy = MockContextDestroy(monkeypatch)

    ctx = MungeContext()
    assert not ctx.closed
    assert ctx.ctx is not None
    ctx_internal = ctx.ctx

    ctx.close()
    assert ctx.closed
    assert ctx.ctx is None
    ctx.close()
    assert ctx.closed
    assert ctx.ctx is None

    assert mock_ctx_destroy.history == [ctx_internal]

def test_context_manager(monkeypatch):
    mock_ctx_destroy = MockContextDestroy(monkeypatch)

    ctx1 = MungeContext()
    assert not ctx1.closed
    assert ctx1.ctx is not None
    ctx1_internal = ctx1.ctx
    with ctx1:
        assert not ctx1.closed
        assert ctx1.ctx == ctx1_internal
    assert ctx1.ctx is None
    assert ctx1.closed

    assert mock_ctx_destroy.history == [ctx1_internal]

    ctx2 = MungeContext()
    assert not ctx2.closed
    assert ctx2.ctx is not None
    ctx2_internal = ctx2.ctx
    with ctx2:
        assert not ctx2.closed
        assert ctx2.ctx == ctx2_internal
        ctx2.close()
        assert ctx2.ctx is None
        assert ctx2.closed
    assert ctx2.closed
    assert ctx2.ctx is None

    assert mock_ctx_destroy.history == [ctx1_internal, ctx2_internal]

def test_autoclose(monkeypatch):
    mock_ctx_destroy = MockContextDestroy(monkeypatch)

    def fn1():
        # ctx should be automatically closed when the function returns
        # (because of MungeContext.__del__)
        ctx = MungeContext()
        return ctx.ctx

    ctx1_internal = fn1()
    assert mock_ctx_destroy.history == [ctx1_internal]

    def fn2():
        ctx = MungeContext()
        result = ctx.ctx
        ctx.close()
        return result

    ctx2_internal = fn2()
    assert mock_ctx_destroy.history == [ctx1_internal, ctx2_internal]

def test_default_options():
    ctx = MungeContext()
    assert ctx.cipher_type == CipherType.Default
    assert ctx.mac_type == MACType.Default
    assert ctx.zip_type == ZipType.Default
    assert ctx.realm is None
    assert ctx.ttl == TTL_DEFAULT
    assert ctx.addr4 == "0.0.0.0"
    assert ctx.encode_time == 0
    assert ctx.decode_time == 0
    assert ctx.uid_restriction == UID_ANY
    assert ctx.gid_restriction == GID_ANY

def test_set_options():
    ctx = MungeContext()
    ctx.cipher_type = CipherType.CAST5
    ctx.mac_type = MACType.RIPEMD160
    ctx.zip_type = ZipType.bzlib
    ctx.realm = "My Pretty Realm"
    ctx.ttl = 42
    ctx.uid_restriction = 105
    ctx.gid_restriction = 1592

    assert ctx.cipher_type == CipherType.CAST5
    assert ctx.mac_type == MACType.RIPEMD160
    assert ctx.zip_type == ZipType.bzlib
    assert ctx.realm == "My Pretty Realm"
    assert ctx.ttl == 42
    assert ctx.addr4 == "0.0.0.0"
    assert ctx.encode_time == 0
    assert ctx.decode_time == 0
    assert ctx.uid_restriction == 105
    assert ctx.gid_restriction == 1592

    ctx.uid_restriction = UID_ANY
    ctx.gid_restriction = GID_ANY
    assert ctx.uid_restriction == UID_ANY
    assert ctx.gid_restriction == GID_ANY

    ctx.realm = None
    assert ctx.realm is None

def test_ctx_clone_options():
    ctx1 = MungeContext()
    ctx1.cipher_type = CipherType.AES256
    assert ctx1.cipher_type == CipherType.AES256
    ctx2 = MungeContext(ctx1)
    ctx3 = MungeContext(ctx1)
    assert ctx2.cipher_type == CipherType.AES256
    ctx2.cipher_type = CipherType.AES128
    assert ctx2.cipher_type == CipherType.AES128
    assert ctx1.cipher_type == CipherType.AES256
    ctx1.close()
    assert ctx2.cipher_type == CipherType.AES128
    assert ctx3.cipher_type == CipherType.AES256

def test_ctx_encode_decode():
    with MungeContext() as ctx:
        cred1 = ctx.encode()
        assert isinstance(cred1, bytes)
        assert cred1.startswith(b'MUNGE:')

        cred2 = ctx.encode()
        assert isinstance(cred2, bytes)
        assert cred2.startswith(b'MUNGE:')
        assert cred2 != cred1

        cred3 = ctx.encode(b'stuff')
        assert isinstance(cred3, bytes)
        assert cred3.startswith(b'MUNGE:')

        ctx.cipher_type = CipherType.CAST5
        ctx.mac_type = MACType.RIPEMD160

        cred4 = ctx.encode(b'more stuff')
        assert isinstance(cred4, bytes)
        assert cred4.startswith(b'MUNGE:')

    my_uid = os.getuid()
    my_gid = os.getgid()

    ctx1 = MungeContext()
    payload1, uid1, gid1 = ctx1.decode(cred1)
    assert payload1 == b''
    assert uid1 == my_uid
    assert gid1 == my_gid
    assert ctx1.cipher_type != CipherType.Default
    assert ctx1.mac_type != MACType.Default
    assert ctx1.mac_type != MACType.Disabled
    assert ctx1.zip_type != ZipType.Default

    ctx2 = MungeContext()
    payload2, uid2, gid2 = ctx2.decode(cred2)
    assert payload2 == b''
    assert uid2 == my_uid
    assert gid2 == my_gid

    ctx3 = MungeContext()
    payload3, uid3, gid3 = ctx3.decode(cred3)
    assert payload3 == b'stuff'
    assert uid3 == my_uid
    assert gid3 == my_gid

    # also test decoding with a context used a context manager
    with MungeContext() as ctx4:
        payload4, uid4, gid4 = ctx4.decode(cred4)
        assert payload4 == b'more stuff'
        assert uid4 == my_uid
        assert gid4 == my_gid
        assert ctx4.cipher_type == CipherType.CAST5
        assert ctx4.mac_type == MACType.RIPEMD160

def test_encode_decode():
    cred1 = encode()
    assert isinstance(cred1, bytes)
    assert cred1.startswith(b'MUNGE:')

    cred2 = encode(b'foobarbaz')
    assert isinstance(cred2, bytes)
    assert cred2.startswith(b'MUNGE:')

    my_uid = os.getuid()
    my_gid = os.getgid()

    payload1, uid1, gid1, ctx1 = decode(cred1)
    assert payload1 == b''
    assert uid1 == my_uid
    assert gid1 == my_gid
    assert ctx1.cipher_type != CipherType.Default
    assert ctx1.mac_type != MACType.Default
    assert ctx1.mac_type != MACType.Disabled
    assert ctx1.zip_type != ZipType.Default

    payload2, uid2, gid2, ctx2 = decode(cred2)
    assert payload2 == b'foobarbaz'
    assert uid2 == my_uid
    assert gid2 == my_gid
    assert ctx2.cipher_type == ctx1.cipher_type
    assert ctx2.mac_type == ctx1.mac_type
    assert ctx2.zip_type == ctx1.zip_type

def test_get_option_on_closed_context_fails():
    with pytest.raises(MungeError) as excinfo:
        ctx = MungeContext()
        ctx.close()
        ctx.cipher_type
    assert excinfo.value.code == MungeErrorCode.EMUNGE_BAD_ARG

def test_set_option_on_closed_context_fails():
    with pytest.raises(MungeError) as excinfo:
        ctx = MungeContext()
        ctx.close()
        ctx.cipher_type = CipherType.AES256
    assert excinfo.value.code == MungeErrorCode.EMUNGE_BAD_ARG

def test_encode_on_closed_context_fails():
    with pytest.raises(MungeError) as excinfo:
        ctx = MungeContext()
        ctx.close()
        ctx.encode()
    assert excinfo.value.code == MungeErrorCode.EMUNGE_BAD_ARG

def test_decode_on_closed_context_fails():
    cred = encode()
    with pytest.raises(MungeError) as excinfo:
        ctx = MungeContext()
        ctx.close()
        ctx.decode(cred)
    assert excinfo.value.code == MungeErrorCode.EMUNGE_BAD_ARG

def test_bad_socket():
    with MungeContext() as ctx:
        ctx.socket = '/this/socket/path/should/really/not/exist'
        with pytest.raises(MungeError) as excinfo:
            cred = ctx.encode()
    assert excinfo.value.code == MungeErrorCode.EMUNGE_SOCKET

def test_credential_replayed():
    cred = encode(b'Fred')

    my_uid = os.getuid()
    my_gid = os.getgid()

    payload1, uid1, gid1, ctx1 = decode(cred)
    assert payload1 == b'Fred'
    assert uid1 == my_uid
    assert gid1 == my_gid

    with pytest.raises(MungeError) as excinfo:
        payload2, uid2, gid2, ctx2 = decode(cred)
    assert excinfo.value.code == MungeErrorCode.EMUNGE_CRED_REPLAYED
    assert isinstance(excinfo.value.result, tuple)
    assert len(excinfo.value.result) == 3
    payload2, uid2, gid2 = excinfo.value.result
    assert payload2 == b'Fred'
    assert uid2 == my_uid
    assert gid2 == my_gid

    with MungeContext() as ctx3:
        with pytest.raises(MungeError) as excinfo:
            payload3, uid3, gid3 = ctx3.decode(cred)
        assert excinfo.value.code == MungeErrorCode.EMUNGE_CRED_REPLAYED
        assert isinstance(excinfo.value.result, tuple)
        assert len(excinfo.value.result) == 3
        payload3, uid3, gid3 = excinfo.value.result
        assert payload3 == b'Fred'
        assert uid3 == my_uid
        assert gid3 == my_gid
        assert ctx3.cipher_type == ctx1.cipher_type
        assert ctx3.mac_type == ctx1.mac_type
        assert ctx3.zip_type == ctx1.zip_type

@pytest.mark.slow
def test_credential_expired():
    with MungeContext() as ctx:
        ctx.ttl = 1
        cred = ctx.encode()

    time.sleep(2)

    with pytest.raises(MungeError) as excinfo:
        payload, uid, gid, ctx = decode(cred)
    assert excinfo.value.code == MungeErrorCode.EMUNGE_CRED_EXPIRED

def test_uid_restriction():
    my_uid = os.getuid()
    my_gid = os.getgid()

    with MungeContext() as ctx:
        ctx.uid_restriction = my_uid + 1
        cred = ctx.encode(b'secrets!')

    with pytest.raises(MungeError) as excinfo:
        payload, uid, gid, ctx = decode(cred)
    assert excinfo.value.code == MungeErrorCode.EMUNGE_CRED_UNAUTHORIZED
    assert isinstance(excinfo.value.result, tuple)
    assert len(excinfo.value.result) == 3
    assert excinfo.value.result[0] == b''

def test_gid_restriction():
    my_uid = os.getuid()
    my_gid = os.getgid()

    with MungeContext() as ctx:
        ctx.gid_restriction = my_gid + 1
        cred = ctx.encode(b'secrets!')

    with pytest.raises(MungeError) as excinfo:
        payload, uid, gid, ctx = decode(cred)
    assert excinfo.value.code == MungeErrorCode.EMUNGE_CRED_UNAUTHORIZED
    assert isinstance(excinfo.value.result, tuple)
    assert len(excinfo.value.result) == 3
    assert excinfo.value.result[0] == b''
