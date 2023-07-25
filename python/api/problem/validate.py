from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, TypeVar

from flask import Response, request

from api.problem.dataclass import ProblemContent, ProblemHeadWithoutPid
from util import make_simple_error_response

T = TypeVar("T")
@dataclass
class ProblemPayload:
    head: ProblemHeadWithoutPid
    content: ProblemContent


def validate_problem_request_payload_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        if payload is None:
            return make_simple_error_response(
                HTTPStatus.BAD_REQUEST, "Require payload"
            )

        try:
            ProblemPayload(
                head=ProblemHeadWithoutPid(**payload["head"]),
                content=ProblemContent(**payload["content"])
            )
        except Exception:
            return make_simple_error_response(
                HTTPStatus.BAD_REQUEST, "Wrong payload format"
            )

        return func(*args, **kwargs)
    return wrapper