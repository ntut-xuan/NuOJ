from http import HTTPStatus

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index_page_route_should_respond_correct_index_page(client: FlaskClient):
    response: TestResponse = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for index.html -->" in response.text
