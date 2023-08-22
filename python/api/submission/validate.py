from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, TypeVar

from flask import Response, request

from api.submission.dataclass import JudgeResult
from models import Submission
from util import make_simple_error_response

T = TypeVar("T")


def validate_judge_result_payload_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        assert payload is not None

        try:
            JudgeResult(**payload)
        except Exception as e:
            return make_simple_error_response(
                HTTPStatus.BAD_REQUEST, f"Incorrect format of payload: {str(e)}"
            )
        
        return func(*args, **kwargs)
    return wrapper


def validate_submission_should_exists_or_return_forbidden(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        submission_id: int | None = kwargs.get("submission_id")
        
        submission: Submission | None = Submission.query.filter_by(id=submission_id).first()
        
        if submission is None:
            return make_simple_error_response(
                HTTPStatus.FORBIDDEN, "Absent submission ID"
            )
        
        return func(*args, **kwargs)
    return wrapper
