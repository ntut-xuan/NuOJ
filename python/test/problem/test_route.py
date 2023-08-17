from http import HTTPStatus
from json import dumps, loads
from typing import Any
from uuid import uuid4

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from database import db
from models import Language, Problem, ProblemChecker, ProblemSolution, Testcase, User
from storage.util import TunnelCode, is_file_exists, read_file, write_file


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
            dumps(first_problem_payload),
            TunnelCode.PROBLEM,
        )
        write_file(
            "the_second_random_token.json",
            dumps(second_problem_payload),
            TunnelCode.PROBLEM,
        )


@pytest.fixture
def setup_test_user(app: Flask):
    with app.app_context():
        user: User = User(
            user_uid="problem_test_user",
            handle="problem_test_user",
            email="problem@test-user.com",
            password="random_password",
            role=1,
            email_verified=1,
        )
        db.session.add(user)
        db.session.commit()


@pytest.fixture
def setup_problem_to_database(app: Flask):
    with app.app_context():
        first_problem: Problem = Problem(
            problem_id=1,
            problem_token="the_first_random_token",
            problem_author="problem_test_user",
        )
        second_problem: Problem = Problem(
            problem_id=2,
            problem_token="the_second_random_token",
            problem_author="cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd",
        )
        db.session.add(first_problem)
        db.session.add(second_problem)
        db.session.commit()


@pytest.fixture
def setup_problem(
    setup_test_user: None,
    setup_problem_to_database: None,
    setup_problem_to_storage: None,
):
    pass

@pytest.fixture
def setup_langauge(app: Flask):
    with app.app_context():
        language_cpp: Language = Language(
            name="C++14",
            extension="cpp"
        )
        language_py: Language = Language(
            name="Python3",
            extension="py"
        )

        db.session.add(language_cpp)
        db.session.add(language_py)
        db.session.commit()


@pytest.fixture
def setup_problem_solution(app: Flask, setup_langauge: None) -> tuple[str, str]:
    with app.app_context():
        language: str = "Python3"
        problem_solution: ProblemSolution = ProblemSolution(
            id=1,
            language=language,
            filename="1fdd43e9-fad4-4a59-8b9f-e4460e5ae1eb.py"
        )
        db.session.add(problem_solution)
        db.session.commit()

        problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
        assert problem is not None
        problem.problem_solution = 1
        db.session.commit()

        solution_content = "print('Hello World')"
        write_file("1fdd43e9-fad4-4a59-8b9f-e4460e5ae1eb.py", solution_content, TunnelCode.SOLUTION)
        return (solution_content, language)
    

@pytest.fixture
def setup_problem_checker(app: Flask) -> str:
    with app.app_context():
        problem_checker: ProblemChecker = ProblemChecker(
            id=1,
            filename="1fdd43e9-fad4-4a59-8b9f-e4460e5ae1eb.cpp"
        )
        db.session.add(problem_checker)
        db.session.commit()

        problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
        assert problem is not None
        problem.problem_checker = 1
        db.session.commit()

        checker_content = "Some checker content"
        write_file("1fdd43e9-fad4-4a59-8b9f-e4460e5ae1eb.cpp", checker_content, TunnelCode.CHECKER)
        return checker_content


@pytest.fixture
def setup_testcase(app: Flask) -> list[str]:
    with app.app_context():
        filename: str = str(uuid4())
        testcase: Testcase = Testcase(
            id=1,
            filename=filename
        )

        db.session.add(testcase)
        db.session.flush()

        testcase_id: int = testcase.id
        problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
        assert problem is not None
        problem.problem_testcase = testcase_id
        db.session.commit()

        testcase_content: list[str] = ["5", "7", "9"]
        write_file(f"{filename}.json", dumps(testcase_content), TunnelCode.TESTCASE)
        return testcase_content


class TestGetSpecificProblem:
    def test_with_exists_problem_should_respond_the_problem(
        self, client: FlaskClient, setup_problem: None
    ):
        excepted_response_payload: dict[str, dict[str, Any]] = {
            "head": {
                "title": "the_first_problem",
                "problem_pid": 1,
                "time_limit": 1,
                "memory_limit": 48763,
            },
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
            "author": {"user_uid": "problem_test_user", "handle": "problem_test_user"},
        }

        response: TestResponse = client.get("/api/problem/1/")

        assert response.status_code == HTTPStatus.OK
        assert response.json is not None
        assert response.json == excepted_response_payload

    def test_with_absent_problem_should_respond_http_status_forbidden(
        self, client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = client.get("/api/problem/3/")

        assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_all_problem_should_respond_all_the_problem(
    client: FlaskClient, setup_problem: None
):
    excepted_response_payload: list[dict[str, Any]] = [
        {
            "head": {
                "title": "the_first_problem",
                "problem_pid": 1,
                "time_limit": 1,
                "memory_limit": 48763,
            },
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
            "author": {
                "user_uid": "problem_test_user",
                "handle": "problem_test_user",
            },
        },
        {
            "head": {
                "title": "the_second_problem",
                "problem_pid": 2,
                "time_limit": 3,
                "memory_limit": 48763,
            },
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
            "author": {
                "user_uid": "cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd",
                "handle": "test_account",
            },
        },
    ]

    response: TestResponse = client.get("/api/problem/")

    assert response.status_code == HTTPStatus.OK
    assert response.json is not None
    assert response.json == excepted_response_payload


class TestAddProblem:
    def test_should_add_the_problem_into_database(
        self, app: Flask, logged_in_client: FlaskClient
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_second_problem",
                "time_limit": 3,
                "memory_limit": 48763,
            },
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
        }

        response: TestResponse = logged_in_client.post("/api/problem/", json=payload)

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            problem: Problem | None = Problem.query.filter_by(problem_id=1).first()
            assert problem is not None
            assert problem.problem_author == "cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd"

    def test_should_add_the_storage_data(
        self, app: Flask, logged_in_client: FlaskClient
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_second_problem",
                "time_limit": 3,
                "memory_limit": 48763,
            },
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
        }

        response: TestResponse = logged_in_client.post("/api/problem/", json=payload)

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            problem: Problem | None = Problem.query.filter_by(problem_id=1).first()
            assert problem is not None
            storage_file_data: dict[str, Any] = loads(
                read_file(f"{problem.problem_token}.json", TunnelCode.PROBLEM)
            )
            assert storage_file_data["head"] == payload["head"]
            assert storage_file_data["content"] == payload["content"]

    def test_with_wrong_payload_should_return_http_status_bad_request(
        self, app: Flask, logged_in_client: FlaskClient
    ):
        payload: dict[str, Any] = {
            "bla": ":)",
        }

        response: TestResponse = logged_in_client.post("/api/problem/", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_invalid_time_limit_should_return_http_status_bad_request(
        self,
        logged_in_client: FlaskClient,
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_second_problem",
                "time_limit": -1,
                "memory_limit": 48763,
            },
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
        }

        response: TestResponse = logged_in_client.post("/api/problem/", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_invalid_memory_limit_should_return_http_status_bad_request(
        self,
        logged_in_client: FlaskClient,
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_second_problem",
                "time_limit": 10,
                "memory_limit": -1,
            },
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
        }

        response: TestResponse = logged_in_client.post("/api/problem/", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_invalid_title_should_return_http_status_bad_request(
        self,
        logged_in_client: FlaskClient,
    ):
        payload: dict[str, Any] = {
            "head": {"title": "", "time_limit": 10, "memory_limit": 48763},
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
        }

        response: TestResponse = logged_in_client.post("/api/problem/", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_unauthorized_should_return_http_status_unauthorized(
        self, app: Flask, client: FlaskClient
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_second_problem",
                "time_limit": 3,
                "memory_limit": 48763,
            },
            "content": {
                "description": "some_description",
                "input_description": "some_input_description",
                "output_description": "some_output_description",
                "note": "some_note",
            },
        }

        response: TestResponse = client.post("/api/problem/", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_no_paylaod_should_return_http_status_bad_request(
        self, app: Flask, logged_in_client: FlaskClient
    ):
        response: TestResponse = logged_in_client.post("/api/problem/")

        assert response.status_code == HTTPStatus.BAD_REQUEST


class TestUpdateProblem:
    def test_should_update_the_problem(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_third_problem",
                "time_limit": 3,
                "memory_limit": 48763,
            },
            "content": {
                "description": "another_another_description",
                "input_description": "another_another_input_description",
                "output_description": "another_another_output_description",
                "note": "another_another_note",
            },
        }

        response: TestResponse = logged_in_client.put("/api/problem/2/", json=payload)

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            problem_storage_raw_text: str = read_file(
                "the_second_random_token.json", TunnelCode.PROBLEM
            )
            problem_storage_data = loads(problem_storage_raw_text)
            assert problem_storage_data["head"] == payload["head"]
            assert problem_storage_data["content"] == payload["content"]

    def test_with_unauthorized_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_third_problem",
                "time_limit": 3,
                "memory_limit": 48763,
            },
            "content": {
                "description": "another_another_description",
                "input_description": "another_another_input_description",
                "output_description": "another_another_output_description",
                "note": "another_another_note",
            },
        }

        response: TestResponse = client.put("/api/problem/2/", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_no_payload_should_return_http_status_code_bad_request(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = logged_in_client.put("/api/problem/2/")

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_invalid_format_should_return_http_status_code_bad_request(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {"hi": ":)"}

        response: TestResponse = logged_in_client.put("/api/problem/2/", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_invalid_time_limit_should_return_http_status_code_bad_request(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_third_problem",
                "time_limit": -1,
                "memory_limit": 48763,
            },
            "content": {
                "description": "another_another_description",
                "input_description": "another_another_input_description",
                "output_description": "another_another_output_description",
                "note": "another_another_note",
            },
        }

        response: TestResponse = logged_in_client.put("/api/problem/2/", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_invalid_memory_limit_should_return_http_status_code_bad_request(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_third_problem",
                "time_limit": 10,
                "memory_limit": -1,
            },
            "content": {
                "description": "another_another_description",
                "input_description": "another_another_input_description",
                "output_description": "another_another_output_description",
                "note": "another_another_note",
            },
        }

        response: TestResponse = logged_in_client.put("/api/problem/2/", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_invalid_title_should_return_http_status_code_bad_request(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "head": {"title": "", "time_limit": 10, "memory_limit": -1},
            "content": {
                "description": "another_another_description",
                "input_description": "another_another_input_description",
                "output_description": "another_another_output_description",
                "note": "another_another_note",
            },
        }

        response: TestResponse = logged_in_client.put("/api/problem/2/", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_absent_problem_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_third_problem",
                "time_limit": 3,
                "memory_limit": 48763,
            },
            "content": {
                "description": "another_another_description",
                "input_description": "another_another_input_description",
                "output_description": "another_another_output_description",
                "note": "another_another_note",
            },
        }

        response: TestResponse = logged_in_client.put("/api/problem/88/", json=payload)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_author_account_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "head": {
                "title": "the_third_problem",
                "time_limit": 3,
                "memory_limit": 48763,
            },
            "content": {
                "description": "another_another_description",
                "input_description": "another_another_input_description",
                "output_description": "another_another_output_description",
                "note": "another_another_note",
            },
        }

        response: TestResponse = logged_in_client.put("/api/problem/1/", json=payload)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestDeleteProblem:
    def test_should_delete_the_problem(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = logged_in_client.delete("/api/problem/2/")

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            assert not is_file_exists("the_second_problem.json", TunnelCode.PROBLEM)
            problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
            assert problem is None

    def test_with_unauthorized_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = client.delete("/api/problem/2/")

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_absent_id_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = logged_in_client.delete("/api/problem/88/")

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_author_account_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = logged_in_client.delete("/api/problem/1/")

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestGetProblemSolution:
    def test_with_valid_problem_id_should_return_http_status_code_ok(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_problem_solution: tuple[str, str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/solution")

        assert response.status_code == HTTPStatus.OK

    def test_with_valid_problem_id_should_return_problem_solution_content(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_problem_solution: tuple[str, str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/solution")

        assert response.status_code == HTTPStatus.OK
        payload: dict[str, Any] | None = response.get_json(silent=True)
        assert payload is not None
        solution: str = setup_problem_solution[0]
        language: str = setup_problem_solution[1]
        assert payload["content"] == solution
        assert payload["language"] == language

    def test_with_valid_problem_id_and_empty_solution_should_return_empty_problem_solution_content(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/solution")

        assert response.status_code == HTTPStatus.OK
        payload: dict[str, Any] | None = response.get_json(silent=True)
        assert payload is not None
        assert payload["content"] == ""

    def test_with_invalid_problem_id_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_problem_solution: tuple[str, str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/999/solution")

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_problem: None, setup_problem_solution: tuple[str, str]
    ):
        response: TestResponse = client.get("/api/problem/2/solution")

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_not_owner_problem_id_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_problem_solution: tuple[str, str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/1/solution")

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestSetupProblemSolution:
    def test_with_valid_payload_should_return_http_status_code_ok(
        self, app: Flask, logged_in_client: FlaskClient, setup_langauge: None, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
            "language": "C++14"
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/solution", json=payload)

        assert response.status_code == HTTPStatus.OK

    def test_with_valid_payload_should_setup_data_into_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_langauge: None, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
            "language": "C++14"
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/solution", json=payload)

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
            assert problem is not None
            assert problem.problem_solution == 1 # We assume the ID of ProblemSolution is 1 since it's the first ProblemSolution we added.
            problem_solution: ProblemSolution | None = ProblemSolution.query.filter_by(id=1).first()
            assert problem_solution is not None
            assert len(problem_solution.filename) == len(str(uuid4())) # We ignore to check the value instead of check the length is valid.
            assert problem_solution.language == "C++14"

    def test_with_valid_payload_should_add_the_solution_file_to_storage(
        self, app: Flask, logged_in_client: FlaskClient, setup_langauge: None, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
            "language": "C++14"
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/solution", json=payload)

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
            assert problem is not None
            problem_solution: ProblemSolution | None = ProblemSolution.query.filter_by(id=problem.problem_solution).first()
            assert problem_solution is not None
            filename: str = problem_solution.filename
            language: Language | None = Language.query.filter_by(name=problem_solution.language).first()
            assert language is not None
            content: str = read_file(f"{filename}.{language.extension}", TunnelCode.SOLUTION)
            assert content == payload["content"]

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, setup_langauge: None, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
            "language": "C++14"
        }

        response: TestResponse = client.post("/api/problem/2/solution", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_invalid_payload_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, setup_langauge: None, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "invalid payload": "absolutely"
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/solution", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_unregister_language_should_return_http_status_code_unprocessable_entity(
        self, logged_in_client: FlaskClient, setup_langauge: None, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
            "language": "Unregister Language"
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/solution", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_absent_problem_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_langauge: None, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
            "language": "C++14"
        }

        response: TestResponse = logged_in_client.post("/api/problem/888/solution", json=payload)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_owner_problem_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_langauge: None, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
            "language": "C++14"
        }

        response: TestResponse = logged_in_client.post("/api/problem/1/solution", json=payload)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestSetupProblemChecker:
    def test_with_valid_payload_should_return_http_status_code_ok(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some checker content",
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/checker", json=payload)

        assert response.status_code == HTTPStatus.OK

    def test_with_valid_payload_should_setup_data_into_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some checker content",
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/checker", json=payload)

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
            assert problem is not None
            assert problem.problem_checker == 1 # We assume the ID of ProblemChecker is 1 since it's the first ProblemChecker we added.
            problem_checker: ProblemChecker | None = ProblemChecker.query.filter_by(id=1).first()
            assert problem_checker is not None
            assert len(problem_checker.filename) == len(str(uuid4())) # We ignore to check the value instead of check the length is valid.

    def test_with_valid_payload_should_add_the_solution_file_to_storage(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/checker", json=payload)

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
            assert problem is not None
            problem_checker: ProblemChecker | None = ProblemChecker.query.filter_by(id=problem.problem_checker).first()
            assert problem_checker is not None
            filename: str = problem_checker.filename
            content: str = read_file(f"{filename}.cpp", TunnelCode.CHECKER)
            assert content == payload["content"]

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
        }

        response: TestResponse = client.post("/api/problem/2/checker", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_invalid_payload_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "invalid payload": "absolutely"
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/checker", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_absent_problem_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
        }

        response: TestResponse = logged_in_client.post("/api/problem/888/checker", json=payload)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_owner_problem_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "content": "Some answer content",
        }

        response: TestResponse = logged_in_client.post("/api/problem/1/checker", json=payload)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestGetProblemChecker:
    def test_with_valid_problem_id_should_return_http_status_code_ok(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_problem_checker: str
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/checker")

        assert response.status_code == HTTPStatus.OK

    def test_with_valid_problem_id_should_return_problem_checker_content(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_problem_checker: str
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/checker")

        assert response.status_code == HTTPStatus.OK
        payload: dict[str, Any] | None = response.get_json(silent=True)
        assert payload is not None
        checker_content: str = setup_problem_checker
        assert payload["content"] == checker_content

    def test_with_valid_problem_id_and_empty_checker_should_return_empty_problem_solution_content(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/checker")

        assert response.status_code == HTTPStatus.OK
        payload: dict[str, Any] | None = response.get_json(silent=True)
        assert payload is not None
        assert payload["content"] == ""

    def test_with_invalid_problem_id_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_problem_checker: str
    ):
        response: TestResponse = logged_in_client.get("/api/problem/999/checker")

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_problem: None, setup_problem_checker: str
    ):
        response: TestResponse = client.get("/api/problem/2/solution")

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_not_owner_problem_id_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_problem_solution: tuple[str, str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/1/solution")

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestGetTestcase:
    def test_with_valid_problem_id_should_return_http_status_code_ok(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_testcase: list[str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/testcase")

        assert response.status_code == HTTPStatus.OK

    def test_with_valid_problem_id_should_return_correct_response(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_testcase: list[str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/testcase")

        assert response.status_code == HTTPStatus.OK
        response_payload: dict[str, Any] | None = response.get_json(silent=True)
        assert response_payload is not None
        assert loads(response_payload["testcase"]) == setup_testcase

    def test_with_not_setup_testcase_should_return_empty_testcase(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        response: TestResponse = logged_in_client.get("/api/problem/2/testcase")

        assert response.status_code == HTTPStatus.OK
        response_payload: dict[str, Any] | None = response.get_json(silent=True)
        assert response_payload is not None
        assert loads(response_payload["testcase"]) == []

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_problem: None, setup_testcase: list[str]
    ):
        response: TestResponse = client.get("/api/problem/2/testcase")

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_absent_problem_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_testcase: list[str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/888/testcase")

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_owner_problem_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None, setup_testcase: list[str]
    ):
        response: TestResponse = logged_in_client.get("/api/problem/1/testcase")

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestSetupTestcase:
    def test_with_valid_payload_should_return_http_status_code_ok(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "testcase": ["3", "5", "8"]
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/testcase", json=payload)

        assert response.status_code == HTTPStatus.OK

    def test_with_valid_payload_should_add_record_into_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        with app.app_context():
            payload: dict[str, Any] = {
                "testcase": ["3", "5", "8"]
            }

            response: TestResponse = logged_in_client.post("/api/problem/2/testcase", json=payload)

            assert response.status_code == HTTPStatus.OK
            problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
            assert problem is not None
            testcase_id = problem.problem_testcase
            assert testcase_id == 1
            testcase_from_database: Testcase | None = Testcase.query.filter_by(id=testcase_id).first()
            assert testcase_from_database is not None
            filename: str = testcase_from_database.filename
            assert len(filename) == len(str(uuid4()))

    def test_with_valid_payload_should_setup_testcase_file(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        with app.app_context():
            payload: dict[str, Any] = {
                "testcase": ["3", "5", "8"]
            }

            response: TestResponse = logged_in_client.post("/api/problem/2/testcase", json=payload)

            assert response.status_code == HTTPStatus.OK
            problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
            assert problem is not None
            testcase_id = problem.problem_testcase
            testcase_from_database: Testcase | None = Testcase.query.filter_by(id=testcase_id).first()
            assert testcase_from_database is not None
            filename: str = testcase_from_database.filename
            testcase_raw_text = read_file(f"{filename}.json", TunnelCode.TESTCASE)
            testcase_payload: list[str] = loads(testcase_raw_text)
            assert testcase_payload == payload["testcase"]

    def test_with_invalid_payload_should_return_http_status_code_bad_request(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "invalid_payload": "absolutly"
        }

        response: TestResponse = logged_in_client.post("/api/problem/2/testcase", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "invalid_payload": "absolutly"
        }

        response: TestResponse = client.post("/api/problem/2/testcase", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_not_owner_problem_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_problem: None
    ):
        payload: dict[str, Any] = {
            "testcase": ["3", "5", "8"]
        }

        response: TestResponse = logged_in_client.post("/api/problem/1/testcase", json=payload)

        assert response.status_code == HTTPStatus.FORBIDDEN