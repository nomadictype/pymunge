import enum

class MungeErrorCode(enum.Enum):
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
        if not isinstance(code, MungeErrorCode):
            code = MungeErrorCode(code)
        super().__init__("%s (error code %d: %s)" % (message, code.value, code.name))
        self.code = code
        self.message = message
        self.result = result
