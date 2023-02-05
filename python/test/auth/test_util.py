import pytest
from flask import Flask

from api.auth.auth_util import login, register
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
