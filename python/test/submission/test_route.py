import datetime
import json
from http import HTTPStatus
from typing import Any
from uuid import uuid4

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from api.submission.dataclass import JudgeDetail, JudgeResult, JudgeMeta
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
def cce_payload():
    with open("./test/submission/response/cce_response.json", "r") as file:
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
def sce_payload():
    with open("./test/submission/response/sce_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def sre_payload():
    with open("./test/submission/response/sre_response.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def smle_payload():
    with open("./test/submission/response/smle_response.json", "r") as file:
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
    app: Flask, setup_langauge: None, solution: str, checker: str, setup_problem_to_storage: None
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
def setup_problem_to_storage(app: Flask):
    first_problem_payload: dict[str, Any] = {
        "head": {"title": "the_first_problem", "time_limit": 1, "memory_limit": 48763},
        "content": {
            "description": "some_description",
            "input_description": "some_input_description",
            "output_description": "some_output_description",
            "note": "some_note",
        },
    }
    second_problem_payload: dict[str, Any] = {
        "head": {"title": "the_second_problem", "time_limit": 3, "memory_limit": 48763},
        "content": {
            "description": "some_description",
            "input_description": "some_input_description",
            "output_description": "some_output_description",
            "note": "some_note",
        },
    }

    with app.app_context():
        write_file(
            "the_first_random_token.json",
            json.dumps(first_problem_payload),
            TunnelCode.PROBLEM,
        )
        write_file(
            "the_second_random_token.json",
            json.dumps(second_problem_payload),
            TunnelCode.PROBLEM,
        )


@pytest.fixture
def setup_submission(app: Flask, setup_problem_to_database: None) -> str:
    tracker_uid: str = "d4f79fdc-5b73-43fe-a249-540873cd1d9e"

    with app.app_context():
        submission: Submission = Submission(
            user_uid="cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd",
            problem_id=1,
            date=datetime.date(2002, 6, 25),
            compiler="c++14",
            tracker_uid=tracker_uid,
        )

        db.session.add(submission)
        db.session.commit()

    return tracker_uid


@pytest.fixture
def setup_verdict(app: Flask) -> None:
    tracker_uid: str = "d4f79fdc-5b73-43fe-a249-540873cd1d9e"

    with app.app_context():
        verdict: Verdict = Verdict(
            id=1,
            tracker_uid=tracker_uid,
            date=datetime.date(2002, 6, 25),
            verdict="AC",
            error_id=None,
            memory_usage=131072,
            time_usage=10
        )

        db.session.add(verdict)
        db.session.commit()


def fetch_memory_average_usage(payload: dict[str, Any]) -> int:
    judge_result: JudgeResult = JudgeResult(**payload)
    memory = 0

    judge_details: list[JudgeDetail] | None = judge_result.data.judge_detail
    assert judge_details

    for judge_detail in judge_details:
        judge_submit_meta: JudgeMeta | None = judge_detail.runtime_info.submit 
        assert judge_submit_meta
        memory += judge_submit_meta.memory

    return memory // len(judge_details)


def fetch_time_average_usage(payload: dict[str, Any]) -> float:
    judge_result: JudgeResult = JudgeResult(**payload)
    time: float = 0

    judge_details: list[JudgeDetail] | None = judge_result.data.judge_detail
    assert judge_details

    for judge_detail in judge_details:
        judge_submit_meta: JudgeMeta | None = judge_detail.runtime_info.submit 
        assert judge_submit_meta
        time += judge_submit_meta.time

    return time / len(judge_details)

class TestGetSubmissions:
    def test_with_record_should_return_status_code_ok(
        self, logged_in_client: FlaskClient, setup_submission: str, setup_verdict: None
    ):
        response: TestResponse = logged_in_client.get("/api/submission")

        assert response.status_code == HTTPStatus.OK

    def test_with_record_hould_return_correct_response(
        self, logged_in_client: FlaskClient, setup_submission: str, setup_verdict: None
    ):
        expected_payload: list[dict[str, Any]] = [
            {
                "id": 1,
                "date": datetime.datetime(2002, 6, 25).strftime('%a, %d %b %Y %H:%M:%S GMT'),
                "user": {
                    "user_id": "cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd",
                    "handle": "test_account",
                    "email": "test_account@nuoj.com"
                },
                "problem": {
                    "problem_id": 1,
                    "title": "the_first_problem"
                },
                "compiler": "c++14",
                "verdict": {
                    "verdict": "AC",
                    "time": 10,
                    "memory": 131072
                }
            }
        ]
        response: TestResponse = logged_in_client.get("/api/submission")

        assert response.status_code == HTTPStatus.OK
        response_json: dict[str, Any] | None = response.get_json(silent=True)
        assert response_json == expected_payload

    def test_with_empty_record_hould_return_correct_response(
        self, logged_in_client: FlaskClient
    ):
        expected_payload: list[dict[str, Any]] = []
        response: TestResponse = logged_in_client.get("/api/submission")

        assert response.status_code == HTTPStatus.OK
        response_json: dict[str, Any] | None = response.get_json(silent=True)
        assert response_json == expected_payload

class TestGetSubmission:
    def test_with_exists_submission_id_should_return_http_status_code_ok(
        self, logged_in_client: FlaskClient, setup_submission: str, setup_verdict: None
    ):
        response: TestResponse = logged_in_client.get("/api/submission/1")

        assert response.status_code == HTTPStatus.OK
    
    def test_with_exists_submission_id_should_return_correct_payload(
        self, logged_in_client: FlaskClient, setup_submission: str, setup_verdict: None
    ):
        response: TestResponse = logged_in_client.get("/api/submission/1")

        assert response.status_code == HTTPStatus.OK
        response_json: dict[str, Any] | None = response.get_json(silent=True)
        assert response_json is not None
        assert response_json["id"] == 1
        assert datetime.datetime.strptime(response_json["date"], '%a, %d %b %Y %H:%M:%S %Z') == datetime.datetime(2002, 6, 25)
        assert response_json["user"] == {
            "user_id": "cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd",
            "handle": "test_account",
            "email": "test_account@nuoj.com"
        }
        assert response_json["problem"] == {
            "problem_id": 1,
            "title": "the_first_problem"
        }
        assert response_json["compiler"] == "c++14"
        assert response_json["verdict"] == {
            "verdict": "AC",
            "time": 10,
            "memory": 131072
        }
    
    def test_with_not_exists_submission_id_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_submission: str, setup_verdict: None
    ):
        response: TestResponse = logged_in_client.get("/api/submission/999")

        assert response.status_code == HTTPStatus.FORBIDDEN


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

    def test_with_cce_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        cce_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=cce_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "CCE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == -1
            assert (
                verdict_error_comment.message
                == "Checker compile failed."
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

    def test_with_sce_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        sce_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=sce_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "SCE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == -1
            assert (
                verdict_error_comment.message
                == "Solution compile failed."
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
            assert verdict.verdict == "SRE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming return exitsig 6"
            )

    def test_with_smle_valid_payload_should_store_correct_data_to_database(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        smle_payload: dict[str, Any],
        setup_submission: str
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submission/1/result", json=smle_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            tracker_uid: str = setup_submission
            verdict: Verdict = Verdict.query.filter_by(tracker_uid=tracker_uid).first()
            assert verdict.verdict == "SMLE"
            assert verdict.error_id == 1
            verdict_error_comment: VerdictErrorComment = (
                VerdictErrorComment.query.filter_by(id=1).first()
            )
            assert verdict_error_comment.failed_testcase_index == 0
            assert (
                verdict_error_comment.message
                == "The programming has reached the memory limit. (10448KB)"
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
