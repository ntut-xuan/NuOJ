from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, Final, TypeVar

from flask import Response, request

from models import User
from util import make_simple_error_response


T = TypeVar("T")


def user_should_exists_or_return_http_status_forbidden(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        name: str = kwargs["name"]

        user: User | None = User.query.filter_by(handle=name).first()

        if user is None:
            return make_simple_error_response(HTTPStatus.FORBIDDEN)

        return func(*args, **kwargs)

    return wrapper


def payload_should_have_correct_format_or_return_http_status_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    
    @dataclass
    class ProfileValidator:
        school: str = ""
        bio: str = ""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        BAD_REQUEST_MESSAGE: Final[str] = "The format of the payload is incorrect."

        if payload is None:
            return make_simple_error_response(HTTPStatus.BAD_REQUEST, BAD_REQUEST_MESSAGE)
        
        try:
            ProfileValidator(**payload)
        except Exception:
            return make_simple_error_response(HTTPStatus.BAD_REQUEST, BAD_REQUEST_MESSAGE)

        return func(*args, **kwargs)

    return wrapper
