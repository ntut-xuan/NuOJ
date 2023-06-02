from http import HTTPStatus
from typing import Final

import pytest
from flask import Flask
from flask.testing import FlaskClient, TestResponse

from database import db
from models import Profile, User
from storage.util import TunnelCode, write_file_bytes

USER_UID: Final[str] = "1490c454-4903-4df6-8321-3125092004a7"
HANDLE: Final[str] = "test_user"
EMAIL: Final[str] = "test_user@nuoj.test"
SCHOOL: Final[str] = "ntut"
BIO: Final[str] = "Hi I'm testing user"
IMG_TYPE: Final[str] = "jpg"

class TestProfileRoute:
    @pytest.fixture()
    def setup_user_and_profile(self, app: Flask):
        with app.app_context():
            user: User = User(
                user_uid=USER_UID,
                handle=HANDLE,
                password="1160130875fda0812c99c5e3f1a03516471a6370c4f97129b221938eb4763e63", #SHA256(test_user)
                email=EMAIL,
                role=1,
                email_verified=1
            )
            db.session.add(user)
            db.session.flush()

            profile: Profile = Profile(
                user_uid=USER_UID,
                img_type=IMG_TYPE,
                email=EMAIL,
                school=SCHOOL,
                bio=BIO
            )

            db.session.add(profile)
            db.session.commit()


    def test_fetch_profile_should_return_correct_profile_response(self, client: FlaskClient, setup_user_and_profile: None):
        excepted_payload: dict[str, str] = {
            "user_uid": USER_UID,
            "email": EMAIL,
            "school": SCHOOL,
            "bio": BIO
        }
        
        response: TestResponse = client.get("/api/profile/test_user")

        assert response.status_code == HTTPStatus.OK
        assert response.json is not None
        assert response.json == excepted_payload

    def test_fetch_profile_with_invalid_user_should_return_http_status_forbidden(self, client: FlaskClient):
        response: TestResponse = client.get("/api/profile/invalid_user")

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_fetch_profile_image_should_return_valid_binary(self, app: Flask, client: FlaskClient, setup_user_and_profile: None):
        with app.app_context():
            write_file_bytes(f"{USER_UID}.{IMG_TYPE}", b"testing_bytes", TunnelCode.USER_AVATER)

        response: TestResponse = client.get("/api/profile/avatar/test_user")

        assert response.status_code == HTTPStatus.OK
        assert response.data == b"testing_bytes"

    def test_fetch_profile_image_with_invalid_user_should_return_http_status_code_forbidden(self, client: FlaskClient):
        response: TestResponse = client.get("/api/profile/avatar/test_user")

        assert response.status_code == HTTPStatus.FORBIDDEN