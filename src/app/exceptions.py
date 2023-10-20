from src.app.constants import ErrorCode
from src.exceptions import BadRequest


class UsernameTaken(BadRequest):
    DETAIL = ErrorCode.USERNAME_TAKEN


class BirthdateNotValid(BadRequest):
    DETAIL = ErrorCode.BIRTHDATE_NOT_VALID
