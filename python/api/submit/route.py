import json
from typing import Any
from uuid import uuid4

import requests
from datetime import datetime
from flask import Blueprint, Response, make_response, request

from api.auth.auth_util import get_user_by_jwt_token
from api.auth.validator import validate_jwt_is_exists_or_return_unauthorized, validate_jwt_is_valid_or_return_unauthorized
from api.submit.validate import validate_problem_can_submit_or_return_unprocessable_entity, validate_submit_payload_or_return_bad_request
from storage.util import TunnelCode, read_file, write_file
from database import db
from models import Language, User, ProblemChecker, Problem, ProblemSolution, Submission, Testcase

submit_bp = Blueprint("submit", __name__, url_prefix="/api/submit")


@submit_bp.route("", methods=["POST"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
@validate_submit_payload_or_return_bad_request
@validate_problem_can_submit_or_return_unprocessable_entity
def submit_route() -> Response:
    payload: dict[str, Any] | None = request.get_json(silent=True)
    assert payload is not None

    user: User = _get_user_with_current_session()
    problem_id: int = payload["problem_id"]
    code: str = payload["code"]
    language: str = payload["language"]

    code_uid: str = str(uuid4())
    submission: Submission = _generate_submission_record(user.user_uid, problem_id, code_uid, language)
    _dumps_submission_code(code, code_uid, language)

    judge_payload: dict[str, Any] = _generate_payload_with_problem(code, language, problem_id, submission.id)
    tracker_uid: str = _send_request_with_payload(judge_payload)
    
    submission.tracker_uid = tracker_uid
    db.session.commit()

    return make_response({"message": "OK"})


def _dumps_submission_code(code: str, code_uid: str, language_str: str):
    language: Language | None = Language.query.filter_by(name=language_str).first()
    assert language is not None

    write_file(f"{code_uid}.{language.extension}", code, TunnelCode.CODE)


def _send_request_with_payload(payload: dict[str, Any]) -> str:
    response: requests.Response = requests.post("http://nuoj-sandbox:4439/api/judge", json=payload)
    response_payload: dict[str, Any] = json.loads(response.text)
    tracker_uid: str = response_payload["tracker_id"]

    return tracker_uid


def _generate_payload_with_problem(code: str, language: str, problem_id: int, submission_id: int):
    problem: Problem | None = Problem.query.filter_by(problem_id=problem_id).first()
    assert problem is not None

    solution, solution_language = _fetch_solution_from_solution_id(problem.problem_solution)
    checker, checker_language = _fetch_checker_from_checker_id(problem.problem_checker)
    testcase = _fetch_testcase_from_testcase_id(problem.problem_testcase)

    payload = _get_judge_payload(code, language, solution, solution_language, checker, checker_language, testcase, submission_id)
    return payload


def _get_judge_payload(user_code: str, user_code_language: str, solution: str, solution_language: str, checker: str, checker_language: str, testcase: list[dict[str, Any]], submission_id: int):
    judge_payload: dict[str, Any] = {
        "user_code": {
            "code": user_code,
            "compiler": user_code_language
        },
        "solution_code": {
            "code": solution,
            "compiler": solution_language
        },
        "checker_code": {
            "code": checker,
            "compiler": checker_language
        },
        "test_case": testcase,
        "execute_type": "Judge",
        "options": {
            "threading": True,
            "time": 10,
            "wall_time": 10,
            "memory": 131072,
            "webhook_url": f"http://nuoj:8080/api/result/{submission_id}"
        }
    }
    return judge_payload


def _generate_submission_record(user_uid: str, problem_id: int, code_uid: str, language: str) -> Submission:
    submission: Submission = Submission(
        user_uid=user_uid,
        problem_id=problem_id,
        date=datetime.now(),
        code_uid=code_uid,
        compiler=language,
    )

    db.session.add(submission)
    db.session.commit()

    return submission


def _fetch_testcase_from_testcase_id(testcase_id: int) -> list[dict[str, Any]]:
    problem_testcase: Testcase | None = Testcase.query.filter_by(id=testcase_id).first()
    assert problem_testcase is not None
    
    filename: str = problem_testcase.filename
    json_text: str = read_file(f"{filename}.json", TunnelCode.TESTCASE)
    testcase_value: list[str] = json.loads(json_text)
    testcase: list[dict[str, Any]] = [{"type": "plain-text", "value": value} for value in testcase_value]
    return testcase


def _fetch_solution_from_solution_id(solution_id: int) -> tuple[str, str]:
    problem_solution: ProblemSolution | None = ProblemSolution.query.filter_by(id=solution_id).first()
    assert problem_solution is not None
    
    filename: str = problem_solution.filename
    language_name: str = problem_solution.language
    language: Language | None = Language.query.filter_by(name=language_name).first()
    assert language is not None
    extension: str = language.extension
    content: str = read_file(f"{filename}.{extension}", TunnelCode.SOLUTION)

    return (content, language_name)


def _fetch_checker_from_checker_id(checker_id: int) -> tuple[str, str]:
    problem_checker: ProblemChecker | None = ProblemChecker.query.filter_by(id=checker_id).first()
    assert problem_checker is not None
    
    filename: str = problem_checker.filename
    content: str = read_file(f"{filename}.cpp", TunnelCode.CHECKER)

    return (content, "c++14")


def _get_user_with_current_session() -> User:
    jwt: str = request.cookies["jwt"]
    
    user: User = get_user_by_jwt_token(jwt)

    return user