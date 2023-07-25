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


def validate_problem_request_payload_is_exist_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        if payload is None:
            return make_simple_error_response(HTTPStatus.BAD_REQUEST, "Require payload")

        return func(*args, **kwargs)

    return wrapper


def validate_problem_request_payload_format_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        assert payload is not None

        try:
            ProblemPayload(
                head=ProblemHeadWithoutPid(**payload["head"]),
                content=ProblemContent(**payload["content"]),
            )
        except Exception:
            return make_simple_error_response(
                HTTPStatus.BAD_REQUEST, "Wrong payload format"
            )

        return func(*args, **kwargs)

    return wrapper


def validate_problem_request_payload_is_valid_or_return_unprocessable_entity(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        assert payload is not None

        try:
            payload: ProblemPayload = ProblemPayload(
                head=ProblemHeadWithoutPid(**payload["head"]),
                content=ProblemContent(**payload["content"]),
            )
            assert len(payload.head.title) > 0
            assert payload.head.time_limit > 0
            assert payload.head.memory_limit > 0
        except Exception:
            return make_simple_error_response(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid time limit or memory limit, or the limit in the payload is reach the max limit.")

        return func(*args, **kwargs)

    return wrapper
