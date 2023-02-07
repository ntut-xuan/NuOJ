import freezegun
import jwt
import pytest
from datetime import timedelta
from flask import Flask, current_app
from pathlib import Path

from api.auth.auth_util import HS256JWTCodec, hash_password, is_user_already_have_handle, login, setup_handle, register
from database import db
from models import User

@pytest.fixture
def setup_test_user(app: Flask) -> None:
    with app.app_context():
        add_user: User = User(
            user_uid="948e2d90-138a-4033-b29b-f15a44fc705d", 
            handle="nuoj", 
            password="cc28a9d01d08f4fa60b63434ce9971fda60e58a2f421898c78582bbb709bf7bb",
            email="nuoj@test.com",
            role=1,
            email_verified=1
        )
        db.session.add(add_user)
        db.session.commit()


class TestLoginUtil:
    def test_with_handle_should_return_true(self, app: Flask, setup_test_user: None):
        with app.app_context():
            is_login: bool = login("nuoj", "nuoj_test")

            assert is_login

    def test_with_email_should_return_true(self, app: Flask, setup_test_user: None):
        with app.app_context():
            is_login: bool = login("nuoj@test.com", "nuoj_test")

            assert is_login

    def test_with_incorrect_password_should_return_false(self, app: Flask, setup_test_user: None):
        with app.app_context():
            is_login: bool = login("nuoj@test.com", "wrong_password")

            assert not is_login


def test_register_with_valid_payload_should_write_data_into_database(app: Flask):
    with app.app_context():

        register("nuoj@test.com", "nuoj_test", "nuoj_test")
        
        user: User | None = User.query.filter_by(email="nuoj@test.com", handle="nuoj_test").first()
        assert user is not None
        assert user.password == "cc28a9d01d08f4fa60b63434ce9971fda60e58a2f421898c78582bbb709bf7bb"

def test_register_with_valid_payload_should_create_profile_file_to_storage(app: Flask):
    with app.app_context():
        
        register("nuoj@test.com", "nuoj_test", "nuoj_test")
        
        user: User | None = User.query.filter_by(email="nuoj@test.com", handle="nuoj_test").first()
        assert user is not None
        user_uid = user.user_uid
        storage_path = current_app.config.get("STORAGE_PATH")
        user_profile_dir_path: Path = Path(storage_path) / "user_profile/"
        assert user_profile_dir_path.exists()
        user_profile_file_path: Path = user_profile_dir_path / ((user_uid) + ".json")
        assert user_profile_file_path.exists()


def test_hash_password_should_return_password_hash_by_sha256_algorithm(app: Flask):
    password = "test_123"
    excepted_hashed_password = "079caa5cce889201054c2eaf61dac76c838d438970bbb71085636d7dc1aba609"
    
    hashed_password = hash_password(password)
    
    assert excepted_hashed_password == hashed_password


def test_setup_handle_should_set_into_database(app: Flask):
    with app.app_context():
        user_without_handle: User = User(user_uid="DOES-NOT-MATTER-ID", handle=None, password="not-matter", email="nuoj@test.com", role=0, email_verified=0)
        db.session.add(user_without_handle)
        db.session.commit()

        setup_handle("nuoj@test.com", "test-handle")
        
        user_with_handle: User | None = User.query.filter(User.email == "nuoj@test.com").first()
        assert user_with_handle is not None
        assert user_with_handle.handle == "test-handle"


def test_user_have_handle_is_already_have_handle_should_return_true(app: Flask):
    with app.app_context():
        user_with_handle: User = User(user_uid="DOES-NOT-MATTER-ID", handle="nuoj", password="not-matter", email="nuoj@test.com", role=0, email_verified=0)
        db.session.add(user_with_handle)
        db.session.commit()
        
        is_user_have_handle = is_user_already_have_handle("nuoj@test.com")
        
        assert is_user_have_handle


def test_user_not_have_handle_is_already_have_handle_should_return_false(app: Flask):
    with app.app_context():
        user_with_handle: User = User(user_uid="DOES-NOT-MATTER-ID", handle=None, password="not-matter", email="nuoj@test.com", role=0, email_verified=0)
        db.session.add(user_with_handle)
        db.session.commit()
        
        is_user_have_handle = is_user_already_have_handle("nuoj@test.com")
        
        assert not is_user_have_handle


class TestHS256JWTCodec:
    @pytest.fixture
    def codec(self) -> HS256JWTCodec:
        return HS256JWTCodec("secret")

    @freezegun.freeze_time("2000-01-01 00:00:00")
    def test_encode(self, codec: HS256JWTCodec) -> None:
        data: dict[str, str] = {"some": "payload"}

        token: str = codec.encode(data, timedelta(days=1))

        expected: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNvbWUiOiJwYXlsb2FkIn0sImlhdCI6OTQ2Njg0ODAwLCJleHAiOjk0Njc3MTIwMH0.FU7fNuSrA-EuVtpE2duW-VD9hJX1B1QfPuQ2_kJ95Lw"
        assert token == expected

    def test_decode(self, codec: HS256JWTCodec) -> None:
        token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg"

        data: dict = codec.decode(token)

        expected: dict[str, str] = {"some": "payload"}
        assert data == expected

    class TestIsValidJWT:
        def test_on_token_with_not_enough_segment_should_return_false(
            self,
            codec: HS256JWTCodec,
        ) -> None:
            token: str = "should_have_three_dot_separated_segments"

            assert not codec.is_valid_jwt(token)

        def test_on_invalid_token_should_return_false(
            self, codec: HS256JWTCodec
        ) -> None:
            token: str = "this.failed.validation"

            assert not codec.is_valid_jwt(token)

        def test_on_expired_token_should_return_false(
            self, codec: HS256JWTCodec
        ) -> None:
            time_to_the_past = timedelta(days=-87)

            token: str = codec.encode({"some": "payload"}, time_to_the_past)

            assert not codec.is_valid_jwt(token)

        def test_on_valid_token_should_return_true(self, codec: HS256JWTCodec) -> None:
            payload: dict[str, str] = {"some": "payload"}
            token: str = jwt.encode(payload, key=codec.key, algorithm=codec.algorithm)

            is_valid_jwt: bool = codec.is_valid_jwt(token)

            assert is_valid_jwt
