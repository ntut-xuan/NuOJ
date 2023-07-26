from http import HTTPStatus
from json import dumps, loads
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from database import db
from models import Problem, User
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


def test_get_specific_problem_with_exists_problem_should_respond_the_problem(
    client: FlaskClient, setup_problem: None
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


def test_get_specific_problem_with_absent_problem_should_respond_http_status_forbidden(
    client: FlaskClient, setup_problem: None
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


def test_add_problem_should_add_the_problem_into_database(
    app: Flask, logged_in_client: FlaskClient
):
    payload: dict[str, Any] = {
        "head": {"title": "the_second_problem", "time_limit": 3, "memory_limit": 48763},
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


def test_add_problem_should_add_the_storage_data(
    app: Flask, logged_in_client: FlaskClient
):
    payload: dict[str, Any] = {
        "head": {"title": "the_second_problem", "time_limit": 3, "memory_limit": 48763},
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


def test_add_problem_with_wrong_payload_should_return_http_status_bad_request(
    app: Flask, logged_in_client: FlaskClient
):
    payload: dict[str, Any] = {
        "bla": ":)",
    }

    response: TestResponse = logged_in_client.post("/api/problem/", json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_add_problem_with_invalid_time_limit_should_return_http_status_bad_request(
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


def test_add_problem_with_invalid_memory_limit_should_return_http_status_bad_request(
    logged_in_client: FlaskClient,
):
    payload: dict[str, Any] = {
        "head": {"title": "the_second_problem", "time_limit": 10, "memory_limit": -1},
        "content": {
            "description": "some_description",
            "input_description": "some_input_description",
            "output_description": "some_output_description",
            "note": "some_note",
        },
    }

    response: TestResponse = logged_in_client.post("/api/problem/", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_add_problem_with_invalid_title_should_return_http_status_bad_request(
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


def test_add_problem_with_unauthorized_should_return_http_status_unauthorized(
    app: Flask, client: FlaskClient
):
    payload: dict[str, Any] = {
        "head": {"title": "the_second_problem", "time_limit": 3, "memory_limit": 48763},
        "content": {
            "description": "some_description",
            "input_description": "some_input_description",
            "output_description": "some_output_description",
            "note": "some_note",
        },
    }

    response: TestResponse = client.post("/api/problem/", json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_add_problem_with_no_paylaod_should_return_http_status_bad_request(
    app: Flask, logged_in_client: FlaskClient
):
    response: TestResponse = logged_in_client.post("/api/problem/")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_problem_should_update_the_problem(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    payload: dict[str, Any] = {
        "head": {"title": "the_third_problem", "time_limit": 3, "memory_limit": 48763},
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


def test_update_problem_with_unauthorized_should_return_http_status_code_unauthorized(
    app: Flask, client: FlaskClient, setup_problem: None
):
    payload: dict[str, Any] = {
        "head": {"title": "the_third_problem", "time_limit": 3, "memory_limit": 48763},
        "content": {
            "description": "another_another_description",
            "input_description": "another_another_input_description",
            "output_description": "another_another_output_description",
            "note": "another_another_note",
        },
    }

    response: TestResponse = client.put("/api/problem/2/", json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_problem_with_no_payload_should_return_http_status_code_bad_request(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    response: TestResponse = logged_in_client.put("/api/problem/2/")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_problem_with_invalid_format_should_return_http_status_code_bad_request(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    payload: dict[str, Any] = {"hi": ":)"}

    response: TestResponse = logged_in_client.put("/api/problem/2/", json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_problem_with_invalid_time_limit_should_return_http_status_code_bad_request(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    payload: dict[str, Any] = {
        "head": {"title": "the_third_problem", "time_limit": -1, "memory_limit": 48763},
        "content": {
            "description": "another_another_description",
            "input_description": "another_another_input_description",
            "output_description": "another_another_output_description",
            "note": "another_another_note",
        },
    }

    response: TestResponse = logged_in_client.put("/api/problem/2/", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_problem_with_invalid_memory_limit_should_return_http_status_code_bad_request(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    payload: dict[str, Any] = {
        "head": {"title": "the_third_problem", "time_limit": 10, "memory_limit": -1},
        "content": {
            "description": "another_another_description",
            "input_description": "another_another_input_description",
            "output_description": "another_another_output_description",
            "note": "another_another_note",
        },
    }

    response: TestResponse = logged_in_client.put("/api/problem/2/", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_problem_with_invalid_title_should_return_http_status_code_bad_request(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
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


def test_update_problem_with_not_author_account_should_return_http_status_code_forbidden(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    payload: dict[str, Any] = {
        "head": {"title": "the_third_problem", "time_limit": 3, "memory_limit": 48763},
        "content": {
            "description": "another_another_description",
            "input_description": "another_another_input_description",
            "output_description": "another_another_output_description",
            "note": "another_another_note",
        },
    }

    response: TestResponse = logged_in_client.put("/api/problem/1/", json=payload)

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_problem_should_delete_the_problem(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    response: TestResponse = logged_in_client.delete("/api/problem/2/")

    assert response.status_code == HTTPStatus.OK
    with app.app_context():
        assert not is_file_exists("the_second_problem.json", TunnelCode.PROBLEM)
        problem: Problem | None = Problem.query.filter_by(problem_id=2).first()
        assert problem is None


def test_delete_problem_with_unauthorized_should_return_http_status_code_unauthorized(
    app: Flask, client: FlaskClient, setup_problem: None
):
    response: TestResponse = client.delete("/api/problem/2/")

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_problem_with_absent_id_should_return_http_status_code_forbidden(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    response: TestResponse = logged_in_client.delete("/api/problem/88/")

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_problem_with_not_author_account_should_return_http_status_code_forbidden(
    app: Flask, logged_in_client: FlaskClient, setup_problem: None
):
    response: TestResponse = logged_in_client.delete("/api/problem/1/")

    assert response.status_code == HTTPStatus.FORBIDDEN
