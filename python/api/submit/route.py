import json
from typing import Any

import requests
from datetime import datetime
from flask import Blueprint, make_response, request

from api.auth.auth_util import get_user_by_jwt_token
from storage.util import TunnelCode, read_file
from database import db
from models import Language, User, ProblemChecker, Problem, ProblemSolution, Submission, Testcase

submit_bp = Blueprint("submit", __name__, url_prefix="/api/submit")


def get_judge_payload(user_code: str, user_code_language: str, solution: str, solution_language: str, checker: str, checker_language: str, testcase: str, submission_id: str):
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


@submit_bp.route("/", methods=["POST"])
def submit_route():
    payload: dict[str, str] = request.get_json(silent=True)
    jwt: str = request.cookies["jwt"]
    
    user: User = get_user_by_jwt_token(jwt)
    problem_id: int = payload["problem_id"]

    submission: Submission = Submission(
        user_id=user.user_uid,
        problem_id=problem_id,
        date=datetime(),
        compiler=payload["language"],
    )

    db.session.add(submission)
    db.session.flush()

    submission_id = submission.id
    problem: Problem | None = Problem.query.filter_by(problem_id=problem_id).first()
    assert problem is not None

    solution, solution_language = _fetch_solution_from_solution_id(problem.problem_solution)
    checker, checker_language = _fetch_checker_from_checker_id(problem.problem_checker)
    testcase = _fetch_testcase_from_testcase_id(problem.problem_testcase)

    payload = get_judge_payload(payload["code"], payload["language"], solution, solution_language, checker, checker_language, testcase, submission_id)
    
    response = requests.post("http://sandbox:4439/judge", json=payload)
    response_payload = response.json()
    tracker_id = response_payload["tracker_id"]

    submission.tracker_uid = tracker_id
    db.session.commit()

    return make_response({"message": "OK"})


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