from libc.time cimport time_t
from posix.stat cimport uid_t, gid_t

cdef extern from "<munge.h>" nogil:
    ctypedef struct munge_ctx:
        pass
    ctypedef munge_ctx* munge_ctx_t

    ctypedef enum munge_opt_t:
        pass
    #    MUNGE_OPT_CIPHER_TYPE       =  0   #: symmetric cipher type (int)
    #    MUNGE_OPT_MAC_TYPE          =  1   #: message auth code type (int)
    #    MUNGE_OPT_ZIP_TYPE          =  2   #: compression type (int)
    #    MUNGE_OPT_REALM             =  3   #: security realm (str)
    #    MUNGE_OPT_TTL               =  4   #: time-to-live (int)
    #    MUNGE_OPT_ADDR4             =  5   #: src IPv4 addr (struct in_addr)
    #    MUNGE_OPT_ENCODE_TIME       =  6   #: time when cred encoded (time_t)
    #    MUNGE_OPT_DECODE_TIME       =  7   #: time when cred decoded (time_t)
    #    MUNGE_OPT_SOCKET            =  8   #: socket for comm w/ daemon (str)
    #    MUNGE_OPT_UID_RESTRICTION   =  9   #: UID able to decode cred (uid_t)
    #    MUNGE_OPT_GID_RESTRICTION   = 10   #: GID able to decode cred (gid_t)

    # ctypedef enum munge_cipher_t:
    #     MUNGE_CIPHER_NONE           =  0   #: encryption disabled
    #     MUNGE_CIPHER_DEFAULT        =  1   #: default ciphr specified by daemon
    #     MUNGE_CIPHER_BLOWFISH       =  2   #: Blowfish CBC w/ 64b-blk/128b-key
    #     MUNGE_CIPHER_CAST5          =  3   #: CAST5 CBC w/ 64b-blk/128b-key
    #     MUNGE_CIPHER_AES128         =  4   #: AES CBC w/ 128b-blk/128b-key
    #     MUNGE_CIPHER_AES256         =  5   #: AES CBC w/ 128b-blk/256b-key
    #     MUNGE_CIPHER_LAST_ITEM

    # ctypedef enum munge_mac_t:
    #     MUNGE_MAC_NONE              =  0   #: mac disabled -- invalid, btw
    #     MUNGE_MAC_DEFAULT           =  1   #: default mac specified by daemon
    #     MUNGE_MAC_MD5               =  2   #: MD5 w/ 128b-digest
    #     MUNGE_MAC_SHA1              =  3   #: SHA-1 w/ 160b-digest
    #     MUNGE_MAC_RIPEMD160         =  4   #: RIPEMD-160 w/ 160b-digest
    #     MUNGE_MAC_SHA256            =  5   #: SHA-256 w/ 256b-digest
    #     MUNGE_MAC_SHA512            =  6   #: SHA-512 w/ 512b-digest
    #     MUNGE_MAC_LAST_ITEM

    # ctypedef enum munge_zip_t:
    #     MUNGE_ZIP_NONE              =  0   #: compression disabled
    #     MUNGE_ZIP_DEFAULT           =  1   #: default zip specified by daemon
    #     MUNGE_ZIP_BZLIB             =  2   #: bzip2 by Julian Seward
    #     MUNGE_ZIP_ZLIB              =  3   #: zlib "deflate" by Gailly & Adler
    #     MUNGE_ZIP_LAST_ITEM

    ctypedef enum munge_enum_t:
        pass
    #    MUNGE_ENUM_CIPHER           =  0   #: cipher enum type
    #    MUNGE_ENUM_MAC              =  1   #: mac enum type
    #    MUNGE_ENUM_ZIP              =  2   #: zip enum type

    ctypedef enum munge_err_t:
        pass
    #    EMUNGE_SUCCESS              =  0   #: Success: Whoohoo!
    #    EMUNGE_SNAFU                =  1   #: Internal error: Doh!
    #    EMUNGE_BAD_ARG              =  2   #: Invalid argument
    #    EMUNGE_BAD_LENGTH           =  3   #: Exceeded maximum message length
    #    EMUNGE_OVERFLOW             =  4   #: Buffer overflow
    #    EMUNGE_NO_MEMORY            =  5   #: Out of memory
    #    EMUNGE_SOCKET               =  6   #: Socket communication error
    #    EMUNGE_TIMEOUT              =  7   #: Socket timeout (NOT USED)
    #    EMUNGE_BAD_CRED             =  8   #: Invalid credential format
    #    EMUNGE_BAD_VERSION          =  9   #: Invalid credential version
    #    EMUNGE_BAD_CIPHER           = 10   #: Invalid cipher type
    #    EMUNGE_BAD_MAC              = 11   #: Invalid MAC type
    #    EMUNGE_BAD_ZIP              = 12   #: Invalid compression type
    #    EMUNGE_BAD_REALM            = 13   #: Unrecognized security realm
    #    EMUNGE_CRED_INVALID         = 14   #: Invalid credential
    #    EMUNGE_CRED_EXPIRED         = 15   #: Expired credential
    #    EMUNGE_CRED_REWOUND         = 16   #: Rewound credential, future ctime
    #    EMUNGE_CRED_REPLAYED        = 17   #: Replayed credential
    #    EMUNGE_CRED_UNAUTHORIZED    = 18   #: Unauthorized credential decode

    munge_err_t munge_encode (char **cred, munge_ctx_t ctx,
                              const void *buf, int len);
    munge_err_t munge_decode (const char *cred, munge_ctx_t ctx,
                              void **buf, int *len, uid_t *uid, gid_t *gid);
    const char * munge_strerror (munge_err_t e);
    munge_ctx_t munge_ctx_create ();
    munge_ctx_t munge_ctx_copy (munge_ctx_t ctx);
    void munge_ctx_destroy (munge_ctx_t ctx);
    const char * munge_ctx_strerror (munge_ctx_t ctx);
    munge_err_t munge_ctx_get (munge_ctx_t ctx, munge_opt_t opt, ...);
    munge_err_t munge_ctx_set (munge_ctx_t ctx, munge_opt_t opt, ...);
    int munge_enum_is_valid (munge_enum_t type, int val);
    const char * munge_enum_int_to_str (munge_enum_t type, int val);
    int munge_enum_str_to_int (munge_enum_t type, const char *str);
