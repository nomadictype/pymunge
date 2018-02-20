from pymunge.enums import *
from pymunge.error import *
from _pymunge import *

result = munge_enum_is_valid(EnumType.Cipher, 5)
print(repr(result))

result = munge_enum_is_valid(CipherType.AES256, 42)
print(repr(result))

result = munge_enum_int_to_str(EnumType.Cipher, 5)
print(repr(result))

result = munge_enum_str_to_int(EnumType.Cipher, 'aes256')
print(repr(result))

result = munge_enum_str_to_int(EnumType.Cipher, b'aes256')
print(repr(result))

result = munge_strerror(MungeErrorCode.EMUNGE_SUCCESS)
print(repr(result))

result = munge_strerror(MungeErrorCode.EMUNGE_SNAFU)
print(repr(result))

ctx = munge_ctx_create()
print(repr(ctx))

#ctx2 = munge_ctx_copy(ctx)
#print(repr(ctx2))

result = munge_ctx_strerror(ctx)
print(repr(result))

print()

errcode, cred = munge_encode(ctx, b'some payload')
print(repr(errcode))
print(repr(cred))
