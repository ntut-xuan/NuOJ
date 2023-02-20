from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from werkzeug.test import TestResponse


def test_login_page_route_should_respond_correct_login_page(client: FlaskClient):

    response: TestResponse = client.get("/login")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for login.html -->" in response.text


def test_register_page_route_should_respond_correct_register_page(client: FlaskClient):

    response: TestResponse = client.get("/register")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for register.html -->" in response.text


def test_handle_setup_page_route_should_respond_correct_handle_setup_page(
    client: FlaskClient,
):

    response: TestResponse = client.get("/handle_setup")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for handle_setup.html -->" in response.text


def test_verify_mail_page_route_should_respond_correct_verify_mail_page(
    client: FlaskClient,
):

    response: TestResponse = client.get("/verify_mail")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for verify_mail.html -->" in response.text
