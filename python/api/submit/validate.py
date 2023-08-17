from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, TypeVar

from flask import Response, request

from models import Problem
from util import make_simple_error_response

T = TypeVar("T")


def validate_submit_payload_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @dataclass
    class PayloadVerification:
        code: str
        language: str
        problem_id: int

    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        assert payload is not None

        try:
            PayloadVerification(**payload)
        except Exception:
            return make_simple_error_response(
                HTTPStatus.BAD_REQUEST, "Incorrect format of payload"
            )
        
        return func(*args, **kwargs)
    return wrapper


def validate_problem_can_submit_or_return_unprocessable_entity(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        assert payload is not None

        problem_id: int = payload["problem_id"]
        problem: Problem = Problem.query.filter_by(problem_id=problem_id).first()

        if(problem.problem_checker == None or problem.problem_solution == None or problem.problem_testcase == None):
            return make_simple_error_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, "Problem is not ready"
            ) 
        
        return func(*args, **kwargs)
    return wrapper