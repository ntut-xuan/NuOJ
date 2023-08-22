import json
from http import HTTPStatus
from typing import Any
from uuid import uuid4

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from api.submission.dataclass import JudgeResult
from database import db
from models import (
    Language,
    Problem,
    ProblemChecker,
    ProblemSolution,
    Submission,
    Verdict,
    VerdictErrorComment,
)
from storage.util import TunnelCode, read_file, write_file


@pytest.fixture
def all_ac_payload():
    with open("./test/submission/response/ac_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def wa_payload():
    with open("./test/submission/response/wa_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def tle_payload():
    with open("./test/submission/response/tle_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def mle_payload():
    with open("./test/submission/response/mle_response.json", "r") as file:
        return json.loads(file.read())
    

@pytest.fixture
def re_payload():
    with open("./test/submission/response/re_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def ce_payload():
    with open("./test/submission/response/ce_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def cmle_payload():
    with open("./test/submission/response/cmle_response.json", "r") as file:
        return json.loads(file.read())
    

@pytest.fixture
def cre_payload():
    with open("./test/submission/response/cre_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def ctle_payload():
    with open("./test/submission/response/ctle_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def sre_payload():
    with open("./test/submission/response/sre_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def code():
    with open("./test/submit/code/code.cpp", "r") as file:
        code = file.read()
        return code


@pytest.fixture
def solution(code: str):
    return code


@pytest.fixture
def checker():
    with open("./test/submit/code/checker.cpp", "r") as file:
        code = file.read()
        return code


@pytest.fixture
def testcase() -> list[str]:
    return ["5", "7"]


@pytest.fixture
def setup_langauge(app: Flask):
    with app.app_context():
        language_cpp: Language = Language(name="c++14", extension="cpp")
        language_py: Language = Language(name="Python3", extension="py")

        db.session.add(language_cpp)
        db.session.add(language_py)
        db.session.commit()


@pytest.fixture
def setup_problem_to_database(
    app: Flask, setup_langauge: None, solution: str, checker: str
):
    solution_uuid: str = str(uuid4())
    checker_uuid: str = str(uuid4())

    with app.app_context():
        problem_checker: ProblemChecker = ProblemChecker(id=1, filename=checker_uuid)
        problem_solution: ProblemSolution = ProblemSolution(
            id=1, language="c++14", filename=solution_uuid
        )
        problem: Problem = Problem(
            problem_id=1,
            problem_token="the_first_random_token",
            problem_author="cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd",
            problem_solution=1,
            problem_checker=1,
            problem_testcase=None,
        )
        db.session.add(problem_checker)
        db.session.add(problem_solution)

        db.session.commit()

        db.session.add(problem)
        db.session.commit()

        write_file(f"{solution_uuid}.cpp", solution, TunnelCode.SOLUTION)
        write_file(f"{checker_uuid}.cpp", checker, TunnelCode.CHECKER)


@pytest.fixture
def setup_submission(app: Flask, setup_problem_to_database: None) -> str:
    tracker_uid: str = str(uuid4())

    with app.app_context():
        submission: Submission = Submission(
            user_uid="cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd",
            problem_id=1,
            compiler="c++14",
            tracker_uid=tracker_uid,
        )

        db.session.add(submission)
        db.session.commit()

    return tracker_uid


def fetch_memory_average_usage(payload: dict[str, Any]) -> int:
    judge_result: JudgeResult = JudgeResult(**payload)
    memory = 0

    for judge_detail in judge_result.data.judge_detail:
        memory += judge_detail.runtime_info.submit.memory

    return memory // len(judge_result.data.judge_detail)


def fetch_time_average_usage(payload: dict[str, Any]) -> float:
    judge_result: JudgeResult = JudgeResult(**payload)
    time: float = 0

    for judge_detail in judge_result.data.judge_detail:
        time += judge_detail.runtime_info.submit.time

    return time / len(judge_result.data.judge_detail)


class TestAddJudgeResult:
    def test_with_valid_payload_should_return_http_status_code_ok(
        self,
        logged_in_client: FlaskClient,
        all_ac_payload: dict[str, Any],
        setup_submission: str,
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=all_ac_payload
        )

        assert response.status_code == HTTPStatus.OK


    def test_with_valid_payload_should_store_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        all_ac_payload: dict[str, Any],
        setup_submission: str,
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=all_ac_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "AC"
            assert verdict.memory_usage == fetch_memory_average_usage(all_ac_payload)
            assert verdict.time_usage == fetch_time_average_usage(all_ac_payload)
            assert verdict.error_id == None


    def test_with_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        wa_payload: dict[str, Any],
        setup_submission: str,
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=wa_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "WA"
            assert verdict.memory_usage == fetch_memory_average_usage(wa_payload)
            assert verdict.time_usage == fetch_time_average_usage(wa_payload)
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "wrong answer 1st lines differ - expected: '1004', found: '14'\n"
            )

    def test_with_tle_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        tle_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=tle_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "TLE"
            assert verdict.memory_usage == fetch_memory_average_usage(tle_payload)
            assert verdict.time_usage == fetch_time_average_usage(tle_payload)
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming has reached the time limit. (10.099s)"
            )

    def test_with_mle_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        mle_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=mle_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "MLE"
            assert verdict.memory_usage == fetch_memory_average_usage(mle_payload)
            assert verdict.time_usage == fetch_time_average_usage(mle_payload)
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming has reached the memory limit. (10428KB)"
            )

    def test_with_re_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        re_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=re_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "RE"
            assert verdict.memory_usage == fetch_memory_average_usage(re_payload)
            assert verdict.time_usage == fetch_time_average_usage(re_payload)
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming return exitsig 6"
            )

    def test_with_ce_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        ce_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=ce_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "CE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == -1
            assert (
                verdict_error_comment.message
                == "Submit code compile failed."
            )

    def test_with_cmle_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        cmle_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=cmle_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "CMLE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming has reached the memory limit. (9656KB)"
            )

    def test_with_cre_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        cre_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=cre_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "CRE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming return exitsig 6"
            )

    def test_with_ctle_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        ctle_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=ctle_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "CTLE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming has reached the time limit. (10.001s)"
            )

    def test_with_sre_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        sre_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=sre_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "CTLE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming has reached the time limit. (10.001s)"
            )

    def test_with_valid_payload_should_store_file_to_storage(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        all_ac_payload: dict[str, Any],
        setup_submission: str,
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=all_ac_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict_payload: str = read_file(
                f"{tracker_uid}.json", TunnelCode.VERDICT
            )
            assert json.loads(verdict_payload) == all_ac_payload


    def test_with_invalid_payload_should_return_http_status_code_bad_request(
        self,
        logged_in_client: FlaskClient,
        all_ac_payload: dict[str, Any],
        setup_submission: str,
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json={"invalid_payload": "absolutly"}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST


    def test_with_invalid_submission_id_should_return_http_status_code_forbidden(
        self,
        logged_in_client: FlaskClient,
        all_ac_payload: dict[str, Any],
        setup_submission: str,
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/999/result", json=all_ac_payload
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
