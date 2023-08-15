import json
from typing import Any

import requests
from datetime import datetime
from flask import Blueprint, Response, make_response, request

from api.auth.auth_util import get_user_by_jwt_token
from storage.util import TunnelCode, read_file
from database import db
from models import Language, User, ProblemChecker, Problem, ProblemSolution, Submission, Testcase

submit_bp = Blueprint("submit", __name__, url_prefix="/api/submit")


@submit_bp.route("/", methods=["POST"])
def submit_route() -> Response:
    payload: dict[str, Any] | None = request.get_json(silent=True)
    assert payload is not None
    jwt: str = request.cookies["jwt"]
    
    user: User = get_user_by_jwt_token(jwt)
    problem_id: int = payload["problem_id"]
    language: str = payload["language"]

    submission: Submission = _generate_submission_record(user.user_uid, problem_id, language)
    submission_id = submission.id

    payload: dict[str, Any] = _generate_payload_with_problem(problem_id, submission_id)
    tracker_uid: str = _send_request_with_payload(payload)
    
    submission.tracker_uid = tracker_uid
    db.session.commit()

    return make_response({"message": "OK"})


def _send_request_with_payload(payload: dict[str, Any]) -> str:
    response = requests.post("http://sandbox:4439/judge", json=payload)
    response_payload = response.json()
    tracker_uid = response_payload["tracker_id"]

    return tracker_uid


def _generate_payload_with_problem(problem_id: int, submission_id: int):
    problem: Problem | None = Problem.query.filter_by(problem_id=problem_id).first()
    assert problem is not None

    solution, solution_language = _fetch_solution_from_solution_id(problem.problem_solution)
    checker, checker_language = _fetch_checker_from_checker_id(problem.problem_checker)
    testcase = _fetch_testcase_from_testcase_id(problem.problem_testcase)

    payload = _get_judge_payload(payload["code"], payload["language"], solution, solution_language, checker, checker_language, testcase, submission_id)


def _get_judge_payload(user_code: str, user_code_language: str, solution: str, solution_language: str, checker: str, checker_language: str, testcase: list[str], submission_id: str):
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
        "testcase": testcase,
        "type": "Judge",
        "options": {
            "threading": True,
            "time": 10,
            "wall_time": 10,
            "memory": 131072,
            "webhook_url": f"http://nuoj:8080/result/{submission_id}"
        }
    }
    return judge_payload


def _generate_submission_record(user_uid: str, problem_id: str, language: str) -> int:
    submission: Submission = Submission(
        user_id=user_uid,
        problem_id=problem_id,
        date=datetime.now(),
        compiler=language,
    )

    db.session.add(submission)
    db.session.commit()

    return submission


def _fetch_testcase_from_testcase_id(testcase_id: int) -> list[str]:
    problem_testcase: Testcase | None = Testcase.query.filter_by(id=testcase_id)
    
    if problem_testcase is None:
        return []
    
    filename: str = problem_testcase.filename
    json_text: str = read_file(f"{filename}.json", TunnelCode.TESTCASE)
    testcase: list[str] = json.loads(json_text)
    return testcase


def _fetch_solution_from_solution_id(solution_id: int) -> tuple[str, str]:
    problem_solution: ProblemSolution | None = ProblemSolution.query.filter_by(id=solution_id).first()
    
    if problem_solution is None:
        return ("", "")
    
    filename: str = problem_solution.filename
    language_name: str = problem_solution.language
    language: Language | None = Language.query.filter_by(name=language_name)
    assert language is not None
    extension: str = language.extension
    content: str = read_file(f"{filename}.{extension}", TunnelCode.SOLUTION)

    return (content, language_name)


def _fetch_checker_from_checker_id(checker_id: int) -> tuple[str, str]:
    problem_checker: ProblemChecker | None = ProblemChecker.query.filter_by(id=checker_id).first()
    
    if problem_checker is None:
        return ("", "")
    
    filename: str = problem_checker.filename
    content: str = read_file(f"{filename}.cpp", TunnelCode.SOLUTION)

    return (content, "cpp")