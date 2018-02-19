/*
 * SWIG interface file (module pymunge_swig)
 *
 * Build with: swig -python pymunge_swig.i
 */

%module pymunge_swig

%{
#define SWIG_FILE_WITH_INIT
#include <munge.h>
%}

munge_err_t munge_encode (char **cred, munge_ctx_t ctx,
                          const void *buf, int len);
munge_err_t munge_decode (const char *cred, munge_ctx_t ctx,
                          void **buf, int *len, uid_t *uid, gid_t *gid);
const char * munge_strerror (munge_err_t e);
munge_ctx_t munge_ctx_create (void);
munge_ctx_t munge_ctx_copy (munge_ctx_t ctx);
void munge_ctx_destroy (munge_ctx_t ctx);
const char * munge_ctx_strerror (munge_ctx_t ctx);
munge_err_t munge_ctx_get (munge_ctx_t ctx, munge_opt_t opt, ...);
munge_err_t munge_ctx_set (munge_ctx_t ctx, munge_opt_t opt, ...);
int munge_enum_is_valid (munge_enum_t type, int val);
const char * munge_enum_int_to_str (munge_enum_t type, int val);
int munge_enum_str_to_int (munge_enum_t type, const char *str);


enum munge_opt_t;
enum munge_enum_t;
