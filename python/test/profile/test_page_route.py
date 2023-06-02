from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from werkzeug.test import TestResponse


def test_profile_page_route_should_respond_correct_profile_page(logged_in_client: FlaskClient):
    response: TestResponse = logged_in_client.get("/profile/test_account")

    assert response.status_code == HTTPStatus.OK
    assert response.text is not None
    assert "<!-- Test mark for profile.html -->" in response.text

