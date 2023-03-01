from http import HTTPStatus

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index_page_route_should_respond_correct_index_page(client: FlaskClient):
    response: TestResponse = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for index.html -->" in response.text


def test_about_page_route_should_respond_correct_about_page(client: FlaskClient):
    response: TestResponse = client.get("/about")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for about.html -->" in response.text


def test_debug_page_route_should_respond_correct_debug_page(client: FlaskClient):
    response: TestResponse = client.get("/debug")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for debug.html -->" in response.text
