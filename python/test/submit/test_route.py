import json
from http import HTTPStatus
from typing import Any
from uuid import uuid4

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from database import db
from models import Language, Problem, ProblemChecker, ProblemSolution, Submission, Testcase
from storage.util import TunnelCode, read_file, write_file


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
def payload(code: str):
    return {"code": code, "language": "c++14", "problem_id": 1}


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
def setup_problem_to_database_with_testcase(
    app: Flask, setup_problem_to_database: None, testcase: list[str]
):
    with app.app_context():
        testcase_uuid: str = str(uuid4())
        problem_testcase: Testcase = Testcase(id=1, filename=testcase_uuid)

        problem: Problem | None = Problem.query.filter_by(problem_id=1).first()
        assert problem is not None
        db.session.add(problem_testcase)
        db.session.commit()

        problem.problem_testcase = 1
        write_file(f"{testcase_uuid}.json", json.dumps(testcase), TunnelCode.TESTCASE)
        db.session.commit()


class TestSubmit:
    def test_submit_route_with_valid_payload_should_return_http_status_code_ok(
        self,
        logged_in_client: FlaskClient,
        payload: dict[str, Any],
        setup_problem_to_database_with_testcase: None,
    ):
        response: TestResponse = logged_in_client.post("/api/submit", json=payload)

        assert response.status_code == HTTPStatus.OK

    def test_submit_route_with_valid_payload_should_dump_the_code(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        payload: dict[str, Any],
        setup_problem_to_database_with_testcase: None,
    ):
        response: TestResponse = logged_in_client.post("/api/submit", json=payload)

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            submission: Submission | None = Submission.query.filter_by(id=1).first()
            assert submission is not None
            language: Language | None = Language.query.filter_by(name=submission.compiler).first()
            assert language is not None
            assert read_file(f"{submission.code_uid}.{language.extension}", TunnelCode.CODE) == payload["code"]

    def test_submit_route_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self,
        client: FlaskClient,
        payload: dict[str, Any],
        setup_problem_to_database_with_testcase: None,
    ):
        response: TestResponse = client.post("/api/submit", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_submit_route_with_invalid_payload_should_return_http_status_code_bad_request(
        self,
        logged_in_client: FlaskClient,
        payload: dict[str, Any],
        setup_problem_to_database_with_testcase: None,
    ):
        response: TestResponse = logged_in_client.post(
            "/api/submit", json={"invalid_payload": "absolutly"}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_submit_route_with_valid_payload_and_empty_testcase_should_return_http_status_code_unprocessable_entity(
        self,
        logged_in_client: FlaskClient,
        payload: dict[str, Any],
        setup_problem_to_database: None,
    ):
        response: TestResponse = logged_in_client.post("/api/submit", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
