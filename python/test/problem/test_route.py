from http import HTTPStatus
from json import dumps
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from database import db
from models import Problem, User
from storage.util import TunnelCode, write_file


@pytest.fixture
def setup_problem_to_storage(app: Flask):
    first_problem_payload: dict[str, Any] = {
        "head": {
            "title": "the_first_problem",
            "problem_pid": 1,
            "time_limit": 1, 
            "memory_limit": 48763
        },
        "content": {
            "description": "some_description",
            "input_description": "some_input_description",
            "output_description": "some_output_description",
            "note": "some_note",
        }
    }
    second_problem_payload: dict[str, Any] = {
        "head": {
            "title": "the_second_problem",
            "problem_pid": 2,
            "time_limit": 3,
            "memory_limit": 48763
        },
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
            problem_author="problem_test_user",
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
            "memory_limit": 48763
        },
        "content": {
            "description": "some_description",
            "input_description": "some_input_description",
            "output_description": "some_output_description",
            "note": "some_note",
        },
        "author": {
            "user_uid": "problem_test_user", 
            "handle": "problem_test_user"
        },
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
                "memory_limit": 48763
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
            }
        },
        {
            "head": {
                "title": "the_second_problem",
                "problem_pid": 2,
                "time_limit": 3,
                "memory_limit": 48763
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
    ]

    response: TestResponse = client.get("/api/problem/")

    assert response.status_code == HTTPStatus.OK
    assert response.json is not None
    assert response.json == excepted_response_payload
