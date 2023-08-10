import requests
from datetime import datetime
from flask import Blueprint, make_response, request

from api.auth.auth_util import get_user_by_jwt_token
from storage.util import TunnelCode, read_file
from database import db
from models import Language, User, ProblemChecker, ProblemSolution, Submission

submit_bp = Blueprint("submit", __name__, url_prefix="/api/submit")


def get_judge_payload(user_code: str, user_code_language: str, solution: str, solution_language: str, checker: str, checker_language: str, submission_id: str):
    judge_payload: dict[str, str] = {
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
    solution, solution_language = fetch_solution_from_problem_id(problem_id)
    checker, checker_language = fetch_checker_from_problem_id(problem_id)
    payload = get_judge_payload(payload["code"], payload["language"], solution, solution_language, checker, checker_language, submission_id)
    
    response = requests.post("http://sandbox:4439/judge", json=payload)
    response_payload = response.json()
    tracker_id = response_payload["tracker_id"]

    submission.tracker_uid = tracker_id
    db.session.commit()

    return make_response({"message": "OK"})


def fetch_solution_from_problem_id(problem_id: int) -> tuple[str, str]:
    problem_solution: ProblemSolution | None = ProblemSolution.query.filter_by(problem_id=problem_id).first()
    
    if problem_solution is None:
        return ""
    
    filename: str = problem_solution.filename
    language_name: str = problem_solution.language
    language: Language | None = Language.query.filter_by(name=language_name)
    extension: str = language.extension
    content: str = read_file(f"{filename}.{extension}", TunnelCode.SOLUTION)

    return (content, language_name)


def fetch_checker_from_problem_id(problem_id: int) -> tuple[str, str]:
    problem_checker: ProblemChecker | None = ProblemChecker.query.filter_by(problem_id=problem_id).first()
    
    if problem_checker is None:
        return ""
    
    filename: str = problem_checker.filename
    content: str = read_file(f"{filename}.cpp", TunnelCode.SOLUTION)

    return (content, "cpp")