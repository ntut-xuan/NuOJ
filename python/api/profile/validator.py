from functools import wraps
from http import HTTPStatus
from typing import Callable, TypeVar

from flask import Response

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