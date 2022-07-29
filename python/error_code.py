from enum import Enum

class ErrorCode(Enum):
    HANDLE_INVALID = 201
    HANDLE_NOT_FOUND = 202
    HANDLE_EXIST = 203
    HANDLE_REPEAT = 204
    EMAIL_INVALID = 302
    EMAIL_NOT_FOUND = 303
    EMAIL_NOT_VERIFICATION = 304
    EMAIL_VERIFICATION_FAILED = 305
    EMAIL_EXIST = 306
    PASSWORD_NOT_MATCH = 401
    PASSWORD_INVALID = 402
    REQUIRE_PAPRMETER = 501
    REQUIRE_AUTHORIZATION = 502
    INVALID_DATA = 601
    UNEXCEPT_ERROR = 999

def error_dict(code: ErrorCode) -> dict:
    return {"status": "Failed", "message": code.name, "code": code.value}