import json
from http import HTTPStatus

from flask import Response

def make_simple_error_response(code: HTTPStatus, message: str = None):
    return Response(json.dumps({"message": message}), status=code)
