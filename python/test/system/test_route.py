from http import HTTPStatus

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

def test_get_heartbeat_should_return_http_status_code_ok(client: FlaskClient):
    response: TestResponse = client.get("/api/heartbeat")

    assert response.status_code == HTTPStatus.OK