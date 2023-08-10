from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, TypeVar

from flask import Response, request

from api.auth.auth_util import get_user_by_jwt_token
from api.problem.dataclass import ProblemContent, ProblemHeadWithoutPid
from models import Language, Problem, User
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
            problem_payload: ProblemPayload = ProblemPayload(
                head=ProblemHeadWithoutPid(**payload["head"]),
                content=ProblemContent(**payload["content"]),
            )
            assert len(problem_payload.head.title) > 0
            assert problem_payload.head.time_limit > 0
            assert problem_payload.head.memory_limit > 0
        except Exception:
            return make_simple_error_response(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                "Invalid time limit or memory limit, or the limit in the payload is reach the max limit.",
            )

        return func(*args, **kwargs)

    return wrapper


def validate_problem_with_specific_id_is_exists_or_return_forbidden(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        problem_id: int | None = kwargs.get("id")
        assert problem_id is not None

        problem: Problem | None = Problem.query.filter_by(problem_id=problem_id).first()

        if problem is None:
            return make_simple_error_response(
                HTTPStatus.FORBIDDEN, "Problem is absent."
            )

        return func(*args, **kwargs)

    return wrapper


def validate_problem_author_is_match_cookies_user_or_return_forbidden(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        jwt: str | None = request.cookies.get("jwt")
        assert jwt is not None
        user: User = get_user_by_jwt_token(jwt)
        problem_id: int | None = kwargs.get("id")
        assert problem_id is not None

        problem: Problem | None = Problem.query.filter_by(problem_id=problem_id).first()
        assert problem is not None

        if problem.problem_author != user.user_uid:
            return make_simple_error_response(
                HTTPStatus.FORBIDDEN, "Permission denied."
            )

        return func(*args, **kwargs)

    return wrapper


def validate_setup_problem_solution_payload_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @dataclass
    class PayloadVerification:
        content: str
        language: str

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


def validate_setup_problem_checker_payload_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @dataclass
    class PayloadVerification:
        content: str

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


def validate_setup_problem_testcase_payload_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @dataclass
    class PayloadVerification:
        testcase: list[str]

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


def validate_language_should_be_exists_or_return_unprocessable_entity(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        assert payload is not None

        language: Language | None = Language.query.filter_by(name=payload["language"]).first()

        if language is None:
            return make_simple_error_response(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid Language (See the information about the avaliable language.)")

        return func(*args, **kwargs)
    return wrapper