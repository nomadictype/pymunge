# cython: c_string_type=str, c_string_encoding=ascii

from . cimport munge

# munge_err_t munge_encode (char **cred, munge_ctx_t ctx,
#                           const void *buf, int len);
# munge_err_t munge_decode (const char *cred, munge_ctx_t ctx,
#                           void **buf, int *len, uid_t *uid, gid_t *gid);
# munge_err_t munge_ctx_get (munge_ctx_t ctx, munge_opt_t opt, ...);
# munge_err_t munge_ctx_set (munge_ctx_t ctx, munge_opt_t opt, ...);

cdef int EMUNGE_SUCCESS = 0

cdef class munge_ctx_t:
    cdef munge.munge_ctx_t ptr

ctypedef munge.munge_err_t munge_err_t

def munge_encode(munge_ctx_t ctx, bytes payload) -> munge_err_t:
    cdef char *cred = NULL
    cdef munge.munge_ctx_t ctx_ptr = ctx.ptr if ctx else NULL
    cdef char *buf = payload
    cdef int length = len(payload)
    cdef munge_err_t errcode
    errcode = munge.munge_encode(&cred, ctx_ptr, buf, length)
    if errcode == EMUNGE_SUCCESS:
        return errcode, <bytes>cred
    else:
        return errcode, None

def munge_strerror(object e) -> str:
    return munge.munge_strerror(e.value)

def munge_ctx_create() -> munge_ctx_t:
    ctx = munge_ctx_t()
    ctx.ptr = munge.munge_ctx_create()
    return ctx

def munge_ctx_copy(munge_ctx_t ctx not None) -> munge_ctx_t:
    ctx2 = munge_ctx_t()
    ctx2.ptr = munge.munge_ctx_copy(ctx.ptr)
    return ctx2

def munge_ctx_destroy(munge_ctx_t ctx not None):
    munge.munge_ctx_destroy(ctx.ptr)

def munge_ctx_strerror(munge_ctx_t ctx not None) -> str:
    cdef const char *s = munge.munge_ctx_strerror(ctx.ptr)
    if s:
        return <str>s
    else:
        return None

def munge_enum_is_valid(object type, int val) -> bool:
    return munge.munge_enum_is_valid(type.value, val) != 0

def munge_enum_int_to_str(object type, int val) -> str:
    return <str>(munge.munge_enum_int_to_str(type.value, val))

def munge_enum_str_to_int(object type, string) -> int:
    return munge.munge_enum_str_to_int(type.value, string)
