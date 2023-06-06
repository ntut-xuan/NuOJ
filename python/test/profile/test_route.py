from http import HTTPStatus
from typing import Final

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from database import db
from models import Profile, User
from storage.util import TunnelCode, write_file_bytes

USER_UID = ""
HANDLE: Final[str] = "test_account"
EMAIL: Final[str] = "test_account@nuoj.test"
SCHOOL: Final[str] = "ntut"
BIO: Final[str] = "Hi I'm testing user"
IMG_TYPE: Final[str] = "jpg"
ROLE: Final[int] = 1

@pytest.fixture(autouse=True)
def get_user_uid(app: Flask):
    with app.app_context():
        global USER_UID
        user: User | None = User.query.filter_by(handle=HANDLE).first()
        
        assert user is not None

        USER_UID = user.user_uid

@pytest.fixture()
def setup_user_and_profile(app: Flask):
    with app.app_context():
        profile: Profile = Profile(
            user_uid=USER_UID,
            img_type=IMG_TYPE,
            email=EMAIL,
            school=SCHOOL,
            bio=BIO,
        )

        db.session.add(profile)
        db.session.commit()


class TestProfileRoute:
    def test_fetch_profile_should_return_correct_profile_response(
        self, client: FlaskClient, setup_user_and_profile: None
    ):
        excepted_payload: dict[str, str | int] = {
            "user_uid": USER_UID,
            "email": EMAIL,
            "school": SCHOOL,
            "bio": BIO,
            "handle": HANDLE,
            "role": ROLE
        }

        response: TestResponse = client.get("/api/profile/test_user")

        assert response.status_code == HTTPStatus.OK
        assert response.json is not None
        assert response.json == excepted_payload

    def test_fetch_profile_with_invalid_user_should_return_http_status_forbidden(
        self, client: FlaskClient
    ):
        response: TestResponse = client.get("/api/profile/invalid_user")

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_fetch_profile_image_should_return_valid_binary(
        self, app: Flask, client: FlaskClient, setup_user_and_profile: None
    ):
        with app.app_context():
            write_file_bytes(
                f"{USER_UID}.{IMG_TYPE}", b"testing_bytes", TunnelCode.USER_AVATER
            )

        response: TestResponse = client.get("/api/profile/test_user/avatar")

        assert response.status_code == HTTPStatus.OK
        assert response.data == b"testing_bytes"

    def test_fetch_profile_image_with_invalid_user_should_return_http_status_code_forbidden(
        self, client: FlaskClient
    ):
        response: TestResponse = client.get("/api/profile/test_user/avatar")

        assert response.status_code == HTTPStatus.FORBIDDEN

class TestUpdateProfile:
    def test_update_profile_with_valid_payload_should_return_http_status_ok(self, app: Flask, logged_in_client: FlaskClient, setup_user_and_profile: None):
        payload: dict[str, str] = {
            "school": "new_school",
            "bio": "Hi this is a new bio."
        }

        response: TestResponse = logged_in_client.put(f"/api/profile/{HANDLE}", json=payload)

        assert response.status_code == HTTPStatus.OK

    def test_update_profile_with_partial_payload_should_return_http_status_ok(self, app: Flask, logged_in_client: FlaskClient, setup_user_and_profile: None):
        payload: dict[str, str] = {
            "school": "new_school",
        }

        response: TestResponse = logged_in_client.put(f"/api/profile/{HANDLE}", json=payload)

        assert response.status_code == HTTPStatus.OK

    def test_update_profile_with_valid_payload_should_update_the_profile(self, app: Flask, logged_in_client: FlaskClient, setup_user_and_profile: None):
        payload: dict[str, str] = {
            "school": "new_school",
            "bio": "Hi this is a new bio."
        }

        logged_in_client.put(f"/api/profile/{HANDLE}", json=payload)

        with app.app_context():
            profile: Profile = Profile.query.filter_by(user_uid=USER_UID).first()
            assert profile.school == payload["school"]
            assert profile.bio == payload["bio"]

    def test_update_profile_with_incorrect_format_payload_should_return_http_status_bad_request(self, logged_in_client: FlaskClient, setup_user_and_profile: None):
        payload: dict[str, str] = {
            "invalid_foramt": "value"
        }

        response: TestResponse = logged_in_client.put(f"/api/profile/{HANDLE}", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST
    
    def test_update_profile_with_incorrect_format_payload_should_return_http_status_bad_request(self, logged_in_client: FlaskClient, setup_user_and_profile: None):
        payload: dict[str, str] = {
            "invalid_foramt": "value"
        }

        response: TestResponse = logged_in_client.put(f"/api/profile/{HANDLE}", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_update_profile_with_unauthorized_should_return_http_status_unauthorized(self, client: FlaskClient):
        payload: dict[str, str] = {
            "school": "new_school",
            "bio": "Hi this is a new bio."
        }

        response: TestResponse = client.put(f"/api/profile/{HANDLE}", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_update_profile_with_not_owner_should_return_http_status_unauthorized(self, app: Flask, client: FlaskClient):
        with app.app_context():
            user: User = User(
                user_uid="d08afcd4-2b7e-4d2f-899e-abad4b76fa2a",
                handle="another_test_user",
                password="e8bf178f625d581191a6bbe4581a0c6779f78bd0ed72ed75c0675777fdbdf2dd", # sha256(another_test_user)
                email="another_test_user@nuoj.net",
                role=0,
                email_verified=1
            )
            db.session.add(user)
            db.session.commit()
            response: TestResponse = client.post(
                "/api/auth/login", json={"account": "another_test_user", "password": "another_test_user"}
            )
            payload: dict[str, str] = {
                "school": "new_school",
                "bio": "Hi this is a new bio."
            }

            response: TestResponse = client.put(f"/api/profile/{HANDLE}", json=payload)

            assert response.status_code == HTTPStatus.FORBIDDEN