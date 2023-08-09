from dataclasses import dataclass
from http import HTTPStatus
from json import dumps, loads
from typing import Any
from uuid import uuid4

from flask import Blueprint, Response, make_response, request
from sqlalchemy.engine.row import Row

from api.auth.auth_util import get_user_by_jwt_token
from api.auth.validator import (
    validate_jwt_is_exists_or_return_unauthorized,
    validate_jwt_is_valid_or_return_unauthorized,
)
from api.problem.dataclass import ProblemHead, ProblemContent, ProblemData
from api.problem.validate import (
    validate_problem_request_payload_is_exist_or_return_bad_request,
    validate_problem_request_payload_format_or_return_bad_request,
    validate_problem_request_payload_is_valid_or_return_unprocessable_entity,
    validate_problem_with_specific_id_is_exists_or_return_forbidden,
    validate_problem_author_is_match_cookies_user_or_return_forbidden,
)
from database import db
from models import Problem, ProblemChecker, ProblemSolution, User
from storage.util import TunnelCode, delete_file, read_file, write_file
from util import make_simple_error_response

problem_bp = Blueprint("problem", __name__, url_prefix="/api/problem")


@problem_bp.route("/<int:id>/", methods=["GET"])
@validate_problem_with_specific_id_is_exists_or_return_forbidden
def get_problems_data_route(id: int) -> Response:
    problem: Problem | None = Problem.query.filter_by(problem_id=id).first()
    assert problem is not None

    problem_pid: str = problem.problem_id

    problem_data: ProblemData = __get_problem_data_object_with_problem_pid(problem_pid)

    return make_response(problem_data.__dict__())


@problem_bp.route("/", methods=["GET"])
def get_all_problems_data_route() -> Response:
    problems: list[Problem] = Problem.query.all()

    payload: list[dict[str, Any]] = [
        __get_problem_data_object_with_problem_pid(problem.problem_id).__dict__()
        for problem in problems
    ]

    return make_response(payload)


@problem_bp.route("/", methods=["POST"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
@validate_problem_request_payload_is_exist_or_return_bad_request
@validate_problem_request_payload_format_or_return_bad_request
@validate_problem_request_payload_is_valid_or_return_unprocessable_entity
def add_problem_data_route() -> Response:
    payload: dict[str, Any] | Any = request.get_json(silent=True)
    assert payload is not None
    jwt: str | None = request.cookies.get("jwt")
    assert jwt is not None
    user: User = get_user_by_jwt_token(jwt)

    # register problem to database
    problem_token: str = str(uuid4())
    problem: Problem = Problem(
        problem_token=problem_token, problem_author=user.user_uid
    )
    db.session.add(problem)
    db.session.commit()

    payload["head"] |= {"problem_pid": problem.problem_id}
    problem_data: ProblemData = ProblemData(
        head=ProblemHead(**payload["head"]),
        content=ProblemContent(**payload["content"]),
        author=user,
    )

    # write content into file
    write_file(
        f"{problem_token}.json",
        dumps(problem_data.__storage_dict__()),
        TunnelCode.PROBLEM,
    )

    # return 200 ok
    return make_response({"message": "OK."})


@problem_bp.route("/<int:id>/", methods=["PUT"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
@validate_problem_request_payload_is_exist_or_return_bad_request
@validate_problem_request_payload_format_or_return_bad_request
@validate_problem_request_payload_is_valid_or_return_unprocessable_entity
@validate_problem_with_specific_id_is_exists_or_return_forbidden
@validate_problem_author_is_match_cookies_user_or_return_forbidden
def update_problem(id: int) -> Response:
    payload: dict[str, Any] | None = request.get_json(silent=True)
    assert payload is not None
    problem: Problem | None = Problem.query.filter_by(problem_id=id).first()
    assert problem is not None
    jwt: str = request.cookies["jwt"]
    user: User = get_user_by_jwt_token(jwt)

    problem_token: str = problem.problem_token
    payload["head"] |= {"problem_pid": problem.problem_id}
    problem_data: ProblemData = ProblemData(
        head=ProblemHead(**payload["head"]),
        content=ProblemContent(**payload["content"]),
        author=user,
    )

    write_file(
        f"{problem_token}.json",
        dumps(problem_data.__storage_dict__()),
        TunnelCode.PROBLEM,
    )
    return make_response({"message": "OK."})


@problem_bp.route("/<int:id>/", methods=["DELETE"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
@validate_problem_with_specific_id_is_exists_or_return_forbidden
@validate_problem_author_is_match_cookies_user_or_return_forbidden
def delete_problem(id: int) -> Response:
    problem: Problem | None = Problem.query.filter_by(problem_id=id).first()
    assert problem is not None

    db.session.delete(problem)
    db.session.commit()

    delete_file(f"{problem.problem_token}.json", tunnel=TunnelCode.PROBLEM)
    return make_response({"message": "OK."})


@problem_bp.route("/<int:id>/solution", methods=["GET"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
@validate_problem_with_specific_id_is_exists_or_return_forbidden
@validate_problem_author_is_match_cookies_user_or_return_forbidden
def get_problem_solution(id: int) -> Response:
    query_row: Row | None = db.session.execute(
        db.select(ProblemSolution.filename, ProblemSolution.language).select_from(Problem).join(ProblemSolution).where(Problem.problem_id == id)
    ).first()

    if query_row is None:
        return make_response({"content": "", "language": ""})
    
    filename: str = query_row.filename
    language: str = query_row.language
    solution_content: str = read_file(filename, TunnelCode.SOLUTION)
    return make_response({"content": solution_content, "language": language})


@problem_bp.route("/<int:id>/checker", methods=["GET"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
@validate_problem_with_specific_id_is_exists_or_return_forbidden
@validate_problem_author_is_match_cookies_user_or_return_forbidden
def get_problem_checker(id: int) -> Response:
    query_row: Row | None = db.session.execute(
        db.select(ProblemChecker.filename).select_from(Problem).join(ProblemChecker).where(Problem.problem_id == id)
    ).first()

    if query_row is None:
        return make_response({"content": ""})
    
    filename: str = query_row.filename
    solution_content: str = read_file(filename, TunnelCode.CHECKER)
    return make_response({"content": solution_content})


def __get_problem_file_data_with_problem_token(problem_token: str) -> dict[str, Any]:
    problem_raw_data: str = read_file(f"{problem_token}.json", TunnelCode.PROBLEM)
    problem_dict: dict[str, Any] = loads(problem_raw_data)

    return problem_dict


def __get_problem_data_object_with_problem_pid(problem_pid: str) -> ProblemData:
    problem: Problem | None = Problem.query.filter_by(problem_id=problem_pid).first()
    assert problem is not None

    problem_id: str = problem.problem_id
    problem_token: str = problem.problem_token
    problem_author: str = problem.problem_author

    user: User | None = User.query.filter_by(user_uid=problem_author).first()
    assert user is not None

    problem_dict = __get_problem_file_data_with_problem_token(problem_token)
    problem_dict["head"] |= {"problem_pid": problem_id}

    problem_data: ProblemData = ProblemData(
        content=ProblemContent(**problem_dict["content"]),
        head=ProblemHead(**problem_dict["head"]),
        author=user,
    )

    return problem_data
