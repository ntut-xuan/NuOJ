import json
from typing import Any
from uuid import uuid4

import requests
from datetime import datetime
from flask import Blueprint, Response, make_response, request

from api.auth.auth_util import get_user_by_jwt_token
from api.auth.validator import validate_jwt_is_exists_or_return_unauthorized, validate_jwt_is_valid_or_return_unauthorized
from api.submit.validate import validate_problem_can_submit_or_return_unprocessable_entity, validate_submit_payload_or_return_bad_request
from api.submit.util import generate_payload_with_problem, send_request_with_payload
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

    judge_payload: dict[str, Any] = generate_payload_with_problem(code, language, problem_id, submission.id)
    tracker_uid: str = send_request_with_payload(judge_payload)
    
    submission.tracker_uid = tracker_uid
    db.session.commit()

    return make_response({"message": "OK"})


def _dumps_submission_code(code: str, code_uid: str, language_str: str):
    language: Language | None = Language.query.filter_by(name=language_str).first()
    assert language is not None

    write_file(f"{code_uid}.{language.extension}", code, TunnelCode.CODE)


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


def _get_user_with_current_session() -> User:
    jwt: str = request.cookies["jwt"]
    
    user: User = get_user_by_jwt_token(jwt)

    return user