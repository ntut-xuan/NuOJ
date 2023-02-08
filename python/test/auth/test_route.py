from typing import Any, ClassVar
from http import HTTPStatus
from http.cookiejar import Cookie, CookieJar

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from api.auth.auth_util import HS256JWTCodec
from models import User
from database import db
from test.util import assert_not_raise

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

class TestLoginRoute:
	def test_with_handle_account_should_respond_http_status_code_ok(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			
			response: TestResponse = client.post("/api/login", json={"account": "nuoj", "password": "nuoj_test"})
			
			assert response.status_code == HTTPStatus.OK
	
	def test_with_handle_account_should_exist_jwt_cookie(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			codec = HS256JWTCodec(app.config["jwt_key"])
			
			response: TestResponse = client.post("/api/login", json={"account": "nuoj", "password": "nuoj_test"})
			
			assert response.status_code == HTTPStatus.OK
			cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
			with assert_not_raise(ValueError):
				(jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
 
	def test_with_handle_account_should_have_correct_jwt_token_attribute(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			codec = HS256JWTCodec(app.config["jwt_key"])
			
			response: TestResponse = client.post("/api/login", json={"account": "nuoj", "password": "nuoj_test"})
			
			assert response.status_code == HTTPStatus.OK
			cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
			(jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
			assert jwt_cookie.value is not None
			jwt_payload: dict[str, Any] = codec.decode(jwt_cookie.value)
			data = jwt_payload["data"]
			assert data["email"] == "nuoj@test.com"
			assert data["handle"] == "nuoj"

	def test_with_email_account_should_respond_http_status_code_ok(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			
			response: TestResponse = client.post("/api/login", json={"account": "nuoj@test.com", "password": "nuoj_test"})
			
			assert response.status_code == HTTPStatus.OK

	def test_with_email_account_should_exist_jwt_cookie(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			codec = HS256JWTCodec(app.config["jwt_key"])
			
			response: TestResponse = client.post("/api/login", json={"account": "nuoj@test.com", "password": "nuoj_test"})
			
			assert response.status_code == HTTPStatus.OK
			cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
			with assert_not_raise(ValueError):
				(jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
 
	def test_with_email_account_should_have_correct_jwt_token_attribute(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			codec = HS256JWTCodec(app.config["jwt_key"])
			
			response: TestResponse = client.post("/api/login", json={"account": "nuoj@test.com", "password": "nuoj_test"})
			
			assert response.status_code == HTTPStatus.OK
			cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
			(jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
			assert jwt_cookie.value is not None
			jwt_payload: dict[str, Any] = codec.decode(jwt_cookie.value)
			data = jwt_payload["data"]
			assert data["email"] == "nuoj@test.com"
			assert data["handle"] == "nuoj"
 
	def test_with_bad_format_payload_should_respond_http_status_code_bad_request(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			
			response: TestResponse = client.post("/api/login", json={"hey": "what"})
			
			assert response.status_code == HTTPStatus.BAD_REQUEST

	def test_with_handle_and_incorrect_password_should_respond_http_status_code_bad_request(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			
			response: TestResponse = client.post("/api/login", json={"account": "nuoj", "password": "wrong_password"})
			
			assert response.status_code == HTTPStatus.FORBIDDEN
			
	def test_with_email_and_incorrect_password_should_respond_http_status_code_bad_request(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			
			response: TestResponse = client.post("/api/login", json={"account": "nuoj@test.com", "password": "wrong_password"})
			
			assert response.status_code == HTTPStatus.FORBIDDEN

class TestRegisterRoute:
	_some_invalid_emails: ClassVar[list[str]] = ["plainaddress", "#@%^%#$@#$@#.com", "@example.com", "Joe Smith <email@example.com>", "email.example.com", "email@example@example.com", ".email@example.com", "email..email@example.com", "email@example.com (Joe Smith)", "email@example", "email@-example.com", "email@111.222.333.44444", "email@example..com", "Abc..123@example.com"]  # fmt: skip
	def test_with_valid_payload_should_respond_http_status_code_ok(self, app: Flask, client: FlaskClient):
		with app.app_context():
			
			response: TestResponse = client.post("/api/register", json={"email": "nuoj@test.com", "handle": "nuoj", "password": "nuoj_test_123"})

			assert response.status_code == HTTPStatus.OK
	
	def test_with_bad_format_payload_should_respond_http_status_code_bad_request(self, app: Flask, client: FlaskClient):
		with app.app_context():
			
			response: TestResponse = client.post("/api/register", json={"hey": "what"})

			assert response.status_code == HTTPStatus.BAD_REQUEST

	@pytest.mark.parametrize(
		argnames="malformed_email",
		argvalues=(
			"noletterafterdash-@email.com",
			"badsymbolindomain@ema#il.com",
			"multipleat@email@org.tw",
			"badsymbol#123@email.com",
			".startwithdot@email.com",
			"double..dot@email.com",
			"domainwithnodot@email",
			"missingat.email.com",
			"あいうえお@example.com",
			*(invalid_email for invalid_email in _some_invalid_emails),
		),
	)
	def test_with_invalid_email_should_respond_http_status_code_unprocessable_entity(self, app: Flask, client: FlaskClient, malformed_email: str):
		with app.app_context():
			
			response: TestResponse = client.post("/api/register", json={"email": malformed_email, "handle": "nuoj", "password": "nuoj_test_123"})

			assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

	@pytest.mark.parametrize(
		argnames="malformed_handle",
		argvalues=(
			"ts", # too short
			"toolooooooooooooooooooooooooooooooooooog",
			"continue-_symbol",
			"continue--symbol",
			"continue__symbol",
			"continue_-symbol",
			"_symbolonfirst",
			"symbolonlast_",
			"-symbolonfirst",
			"symbolonlast-",
			"#invalid_symbol",
		)
	)
	def test_with_invalid_handle_should_respond_http_status_code_unprocessable_entity(self, app: Flask, client: FlaskClient, malformed_handle: str):
		with app.app_context():
			
			response: TestResponse = client.post("/api/register", json={"email": "nuoj@test.com", "handle": malformed_handle, "password": "nuoj_test_123"})

			assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

	@pytest.mark.parametrize(
		argnames="malformed_password",
		argvalues=(
			"ts", # too short
			"just_letter_no_number",
			"123546789",
		)
	)
	def test_with_invalid_password_should_respond_http_status_code_unprocessable_entity(self, app: Flask, client: FlaskClient, malformed_password: str):
		with app.app_context():
			
			response: TestResponse = client.post("/api/register", json={"email": "nuoj@test.com", "handle": "nuoj", "password": malformed_password})

			assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

	def test_with_repeated_email_payload_should_respond_http_status_code_forbidden(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			
			response: TestResponse = client.post("/api/register", json={"email": "nuoj@test.com", "handle": "abcd", "password": "another_password_123"})

			assert response.status_code == HTTPStatus.FORBIDDEN

	def test_with_repeated_handle_payload_should_respond_http_status_code_forbidden(self, app: Flask, client: FlaskClient, setup_test_user: None):
		with app.app_context():
			
			response: TestResponse = client.post("/api/register", json={"email": "another_nuoj@test.com", "handle": "nuoj", "password": "another_password_123"})

			assert response.status_code == HTTPStatus.FORBIDDEN

class TestJWTVerifyRoute:

	def test_with_valid_jwt_token_should_return_http_status_ok(self, logged_in_client: FlaskClient):
		response: TestResponse = logged_in_client.post("/api/verify_jwt")
		
		assert response.status_code == HTTPStatus.OK
		
		
	def test_with_not_exists_jwt_token_should_return_http_status_forbidden(self, client: FlaskClient):
		response: TestResponse = client.post("/api/verify_jwt")
		
		assert response.status_code == HTTPStatus.FORBIDDEN    
		assert response.json is not None 
		assert response.json["message"] == "JWT is not exists."
	
		
	def test_with_not_invalid_jwt_token_should_return_http_status_forbidden(self, client: FlaskClient):
		client.set_cookie("", "jwt", "some.invalid.jwt")
		response: TestResponse = client.post("/api/verify_jwt")
		
		assert response.status_code == HTTPStatus.FORBIDDEN   
		assert response.json is not None 
		assert response.json["message"] == "JWT is invalid."


def _get_cookies(cookie_jar: CookieJar | None) -> tuple[Cookie, ...]:
	if cookie_jar is None:
		return tuple()
	return tuple(cookie for cookie in cookie_jar)
