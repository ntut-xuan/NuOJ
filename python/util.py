import json
from http import HTTPStatus

from flask import Response, make_response


def make_simple_error_response(
    code: HTTPStatus, message: str | None = None
) -> Response:
    return make_response({"message": message}, code)
