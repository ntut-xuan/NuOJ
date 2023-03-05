from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from werkzeug.test import TestResponse


def test_problem_list_page_route_should_respond_correct_problem_list_page(client: FlaskClient):

    response: TestResponse = client.get("/problem")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for problem_list.html -->" in response.text


def test_problem_info_page_route_should_respond_correct_problem_info_page(client: FlaskClient):

    response: TestResponse = client.get("/problem/1")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for problem_info.html -->" in response.text
