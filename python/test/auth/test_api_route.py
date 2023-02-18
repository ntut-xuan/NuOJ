from typing import Any, ClassVar
from http import HTTPStatus
from http.cookiejar import Cookie, CookieJar

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

import api.auth.github_oauth_util
import api.auth.google_oauth_util
from api.auth.auth_util import HS256JWTCodec
from models import User
from database import db
from setting.util import Setting
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
            email_verified=0,
        )
        db.session.add(add_user)
        db.session.commit()


class TestLoginRoute:
    def test_with_handle_account_should_respond_http_status_code_ok(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/login", json={"account": "nuoj", "password": "nuoj_test"}
            )

            assert response.status_code == HTTPStatus.OK

    def test_with_handle_account_should_exist_jwt_cookie(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            codec = HS256JWTCodec(app.config["jwt_key"])

            response: TestResponse = client.post(
                "/api/auth/login", json={"account": "nuoj", "password": "nuoj_test"}
            )

            assert response.status_code == HTTPStatus.OK
            cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
            with assert_not_raise(ValueError):
                (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))

    def test_with_handle_account_should_have_correct_jwt_token_attribute(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            codec = HS256JWTCodec(app.config["jwt_key"])

            response: TestResponse = client.post(
                "/api/auth/login", json={"account": "nuoj", "password": "nuoj_test"}
            )

            assert response.status_code == HTTPStatus.OK
            cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
            (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
            assert jwt_cookie.value is not None
            jwt_payload: dict[str, Any] = codec.decode(jwt_cookie.value)
            data = jwt_payload["data"]
            assert data["email"] == "nuoj@test.com"
            assert data["handle"] == "nuoj"

    def test_with_email_account_should_respond_http_status_code_ok(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/login",
                json={"account": "nuoj@test.com", "password": "nuoj_test"},
            )

            assert response.status_code == HTTPStatus.OK

    def test_with_email_account_should_exist_jwt_cookie(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            codec = HS256JWTCodec(app.config["jwt_key"])

            response: TestResponse = client.post(
                "/api/auth/login",
                json={"account": "nuoj@test.com", "password": "nuoj_test"},
            )

            assert response.status_code == HTTPStatus.OK
            cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
            with assert_not_raise(ValueError):
                (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))

    def test_with_email_account_should_have_correct_jwt_token_attribute(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            codec = HS256JWTCodec(app.config["jwt_key"])

            response: TestResponse = client.post(
                "/api/auth/login",
                json={"account": "nuoj@test.com", "password": "nuoj_test"},
            )

            assert response.status_code == HTTPStatus.OK
            cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
            (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
            assert jwt_cookie.value is not None
            jwt_payload: dict[str, Any] = codec.decode(jwt_cookie.value)
            data = jwt_payload["data"]
            assert data["email"] == "nuoj@test.com"
            assert data["handle"] == "nuoj"

    def test_with_handle_account_but_not_pass_the_mail_verify_should_respond_http_status_code_forbidden(
        self,
        app: Flask,
        client: FlaskClient,
        setup_test_user: None,
        enabled_mail_setting: None,
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/login", json={"account": "nuoj", "password": "nuoj_test"}
            )

            assert response.status_code == HTTPStatus.UNAUTHORIZED
            json_response: dict[str, Any] | None = response.get_json(silent=True)
            assert json_response is not None
            assert (
                json_response["message"]
                == "Mail verification enabled but mail is not verify."
            )

    def test_with_bad_format_payload_should_respond_http_status_code_bad_request(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/login", json={"hey": "what"}
            )

            assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_handle_and_incorrect_password_should_respond_http_status_code_bad_request(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/login",
                json={"account": "nuoj", "password": "wrong_password"},
            )

            assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_email_and_incorrect_password_should_respond_http_status_code_bad_request(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/login",
                json={"account": "nuoj@test.com", "password": "wrong_password"},
            )

            assert response.status_code == HTTPStatus.FORBIDDEN


class TestRegisterRoute:
    _some_invalid_emails: ClassVar[list[str]] = ["plainaddress", "#@%^%#$@#$@#.com", "@example.com", "Joe Smith <email@example.com>", "email.example.com", "email@example@example.com", ".email@example.com", "email..email@example.com", "email@example.com (Joe Smith)", "email@example", "email@-example.com", "email@111.222.333.44444", "email@example..com", "Abc..123@example.com"]  # fmt: skip
    def test_with_valid_payload_should_respond_http_status_code_ok(
        self, app: Flask, client: FlaskClient
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register",
                json={
                    "email": "nuoj@test.com",
                    "handle": "nuoj",
                    "password": "nuoj_test_123",
                },
            )

            assert response.status_code == HTTPStatus.OK

    def test_with_enabled_mail_verification_should_respond_correct_payload_with_mail_verify_status(
        self, app: Flask, client: FlaskClient, enabled_mail_setting: None
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register",
                json={
                    "email": "nuoj@test.com",
                    "handle": "nuoj",
                    "password": "nuoj_test_123",
                },
            )

            assert response.status_code == HTTPStatus.OK
            json_response: dict[str, Any] | None = response.get_json(silent=True)
            assert json_response is not None
            assert json_response["mail_verification_enabled"] == True

    def test_with_disabled_mail_verification_should_respond_correct_payload_with_mail_verify_status(
        self, app: Flask, client: FlaskClient
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register",
                json={
                    "email": "nuoj@test.com",
                    "handle": "nuoj",
                    "password": "nuoj_test_123",
                },
            )

            assert response.status_code == HTTPStatus.OK
            json_response: dict[str, Any] | None = response.get_json(silent=True)
            assert json_response is not None
            assert json_response["mail_verification_enabled"] == False

    def test_with_bad_format_payload_should_respond_http_status_code_bad_request(
        self, app: Flask, client: FlaskClient
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register", json={"hey": "what"}
            )

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
    def test_with_invalid_email_should_respond_http_status_code_unprocessable_entity(
        self, app: Flask, client: FlaskClient, malformed_email: str
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register",
                json={
                    "email": malformed_email,
                    "handle": "nuoj",
                    "password": "nuoj_test_123",
                },
            )

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        argnames="malformed_handle",
        argvalues=(
            "ts",  # too short
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
        ),
    )
    def test_with_invalid_handle_should_respond_http_status_code_unprocessable_entity(
        self, app: Flask, client: FlaskClient, malformed_handle: str
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register",
                json={
                    "email": "nuoj@test.com",
                    "handle": malformed_handle,
                    "password": "nuoj_test_123",
                },
            )

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        argnames="malformed_password",
        argvalues=(
            "ts",  # too short
            "just_letter_no_number",
            "123546789",
        ),
    )
    def test_with_invalid_password_should_respond_http_status_code_unprocessable_entity(
        self, app: Flask, client: FlaskClient, malformed_password: str
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register",
                json={
                    "email": "nuoj@test.com",
                    "handle": "nuoj",
                    "password": malformed_password,
                },
            )

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_repeated_email_payload_should_respond_http_status_code_forbidden(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register",
                json={
                    "email": "nuoj@test.com",
                    "handle": "abcd",
                    "password": "another_password_123",
                },
            )

            assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_repeated_handle_payload_should_respond_http_status_code_forbidden(
        self, app: Flask, client: FlaskClient, setup_test_user: None
    ):
        with app.app_context():
            response: TestResponse = client.post(
                "/api/auth/register",
                json={
                    "email": "another_nuoj@test.com",
                    "handle": "nuoj",
                    "password": "another_password_123",
                },
            )

            assert response.status_code == HTTPStatus.FORBIDDEN


class TestJWTVerifyRoute:
    def test_with_valid_jwt_token_should_return_http_status_ok(
        self, logged_in_client: FlaskClient
    ):
        response: TestResponse = logged_in_client.post("/api/auth/verify_jwt")

        assert response.status_code == HTTPStatus.OK

    def test_with_not_exists_jwt_token_should_return_http_status_forbidden(
        self, client: FlaskClient
    ):
        response: TestResponse = client.post("/api/auth/verify_jwt")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json is not None
        assert response.json["message"] == "JWT is not exists."

    def test_with_not_invalid_jwt_token_should_return_http_status_forbidden(
        self, client: FlaskClient
    ):
        client.set_cookie("", "jwt", "some.invalid.jwt")
        response: TestResponse = client.post("/api/auth/verify_jwt")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json is not None
        assert response.json["message"] == "JWT is invalid."


class TestGithubRoute:
    def test_with_new_account_and_valid_code_should_redirect_to_handle_setup_page(
        self, client: FlaskClient, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "ACCESS_TOKEN_URL",
            "http://0.0.0.0:8080/test/github/access_token",
        )
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "USER_PROFILE_API_URL",
            "http://0.0.0.0:8080/test/github/user_profile",
        )

        response: TestResponse = client.get(
            "/api/auth/github_login", query_string={"code": "valid_code"}
        )

        assert response.status_code == HTTPStatus.FOUND
        assert response.location == "/handle_setup"

    def test_with_old_account_and_valid_code_should_redirect_to_root(
        self, app: Flask, client: FlaskClient, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "ACCESS_TOKEN_URL",
            "http://0.0.0.0:8080/test/github/access_token",
        )
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "USER_PROFILE_API_URL",
            "http://0.0.0.0:8080/test/github/user_profile",
        )
        with app.app_context():
            user: User = User(
                user_uid="random_user_uid",
                handle="some_handle",
                email="oauth_test@nuoj.com",
                password="password",
                role=0,
                email_verified=1,
            )
            db.session.add(user)
            db.session.commit()

        response: TestResponse = client.get(
            "/api/auth/github_login", query_string={"code": "valid_code"}
        )

        assert response.status_code == HTTPStatus.FOUND
        assert response.location == "/"

    def test_with_old_account_and_valid_code_should_have_jwt_cookie(
        self, app: Flask, client: FlaskClient, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "ACCESS_TOKEN_URL",
            "http://0.0.0.0:8080/test/github/access_token",
        )
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "USER_PROFILE_API_URL",
            "http://0.0.0.0:8080/test/github/user_profile",
        )
        codec: HS256JWTCodec = HS256JWTCodec(app.config["jwt_key"])
        user_email: str = "oauth_test@nuoj.com"
        user_handle: str = "some_handle"
        with app.app_context():
            user: User = User(
                user_uid="random_user_uid",
                handle=user_handle,
                email=user_email,
                password="password",
                role=0,
                email_verified=1,
            )
            db.session.add(user)
            db.session.commit()

        response: TestResponse = client.get(
            "/api/auth/github_login", query_string={"code": "valid_code"}
        )

        assert response.status_code == HTTPStatus.FOUND
        cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
        (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
        assert jwt_cookie.value is not None
        jwt_payload: dict[str, Any] = codec.decode(jwt_cookie.value)
        data = jwt_payload["data"]
        assert data["email"] == user_email
        assert data["handle"] == user_handle
    
    def test_with_absent_code_should_return_http_status_code_bad_request(
        self, client: FlaskClient, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "ACCESS_TOKEN_URL",
            "http://0.0.0.0:8080/test/github/access_token",
        )
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "USER_PROFILE_API_URL",
            "http://0.0.0.0:8080/test/github/user_profile",
        )

        response: TestResponse = client.get(
            "/api/auth/github_login"
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_invalid_code_should_return_http_status_code_forbidden(
        self, client: FlaskClient, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "ACCESS_TOKEN_URL",
            "http://0.0.0.0:8080/test/github/access_token",
        )
        monkeypatch.setattr(
            api.auth.github_oauth_util,
            "USER_PROFILE_API_URL",
            "http://0.0.0.0:8080/test/github/user_profile",
        )

        response: TestResponse = client.get(
            "/api/auth/github_login", query_string={"code": "invalid_code"}
        )

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestGoogleRoute:
    @pytest.fixture()
    def monkeypatch_url(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(
            api.auth.google_oauth_util,
            "ACCESS_TOKEN_URL",
            "http://0.0.0.0:8080/test/google/access_token",
        )
        monkeypatch.setattr(
            api.auth.google_oauth_util,
            "USER_PROFILE_API_URL",
            "http://0.0.0.0:8080/test/google/user_profile",
        )

    def test_with_new_account_and_valid_code_should_redirect_to_handle_setup_page(
        self, client: FlaskClient, monkeypatch_url: None
    ):
        response: TestResponse = client.get(
            "/api/auth/google_login", query_string={"code": "valid_code"}
        )

        assert response.status_code == HTTPStatus.FOUND
        assert response.location == "/handle_setup"

    def test_with_new_account_and_valid_code_should_setup_hs_cookie(
        self, app: Flask, client: FlaskClient, monkeypatch_url: None
    ):
        codec: HS256JWTCodec = HS256JWTCodec(app.config["jwt_key"])
        excepted_data_payload_in_cookie: dict[str, str] = {
            "email": "oauth_test@nuoj.com"
        }

        response: TestResponse = client.get(
            "/api/auth/google_login", query_string={"code": "valid_code"}
        )

        assert response.status_code == HTTPStatus.FOUND
        assert _verify_data_field_in_cookie_payload(
            codec, client.cookie_jar, "hs", excepted_data_payload_in_cookie
        )

    def test_with_old_account_and_valid_code_should_redirect_to_root(
        self, app: Flask, client: FlaskClient, monkeypatch_url: None
    ):
        with app.app_context():
            user: User = User(
                user_uid="random_user_uid",
                handle="some_handle",
                email="oauth_test@nuoj.com",
                password="password",
                role=0,
                email_verified=1,
            )
            db.session.add(user)
            db.session.commit()

        response: TestResponse = client.get(
            "/api/auth/google_login", query_string={"code": "valid_code"}
        )

        assert response.status_code == HTTPStatus.FOUND
        assert response.location == "/"

    def test_with_old_account_and_valid_code_should_have_jwt_cookie(
        self, app: Flask, client: FlaskClient, monkeypatch_url: None
    ):
        codec: HS256JWTCodec = HS256JWTCodec(app.config["jwt_key"])
        user_handle: str = "some_handle"
        user_email: str = "oauth_test@nuoj.com"
        excepted_data_payload_in_cookie: dict[str, str] = {
            "email": user_email,
            "handle": user_handle,
        }
        with app.app_context():
            user: User = User(
                user_uid="random_user_uid",
                handle=user_handle,
                email=user_email,
                password="password",
                role=0,
                email_verified=1,
            )
            db.session.add(user)
            db.session.commit()

        response: TestResponse = client.get(
            "/api/auth/google_login", query_string={"code": "valid_code"}
        )

        assert response.status_code == HTTPStatus.FOUND
        assert _verify_data_field_in_cookie_payload(
            codec, client.cookie_jar, "jwt", excepted_data_payload_in_cookie
        )

    def test_with_invalid_code_should_return_http_status_code_forbidden(
        self, client: FlaskClient, monkeypatch_url: None
    ):
        response: TestResponse = client.get(
            "/api/auth/google_login", query_string={"code": "invalid_code"}
        )

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_error_args_should_return_http_status_code_forbidden(
        self, client: FlaskClient, monkeypatch_url: None
    ):
        response: TestResponse = client.get(
            "/api/auth/google_login", query_string={"error": "some_error_message"}
        )

        assert response.status_code == HTTPStatus.FORBIDDEN


def test_logout_with_logged_in_client_should_remove_jwt_token(
    logged_in_client: FlaskClient,
):
    response: TestResponse = logged_in_client.post("/api/auth/logout")

    assert response.status_code == HTTPStatus.OK
    cookies: tuple[Cookie, ...] = _get_cookies(logged_in_client.cookie_jar)
    with pytest.raises(ValueError):
        (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))


class TestOAuthInfoRoute:
    def test_with_enabled_github_oauth_and_google_oauth_should_return_correct_github_oauth_url_and_google_oauth_url_in_json(
        self, app: Flask, client: FlaskClient
    ):
        setting: Setting = app.config["setting"]
        github_client_id = setting.oauth.github.client_id
        google_client_id = setting.oauth.google.client_id
        google_redirect_url = setting.oauth.google.redirect_url
        google_oauth_scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"

        response: TestResponse = client.get("/api/auth/oauth_info")

        response_json: dict[str, str] | None = response.get_json(silent=True)
        assert response_json is not None
        assert (
            response_json["github_oauth_url"]
            == f"https://github.com/login/oauth/authorize?client_id={github_client_id}&scope=repo"
        )
        assert (
            response_json["google_oauth_url"]
            == f"https://accounts.google.com/o/oauth2/v2/auth?client_id={google_client_id}&redirect_uri={google_redirect_url}&response_type=code&scope={google_oauth_scope}"
        )

    def test_with_only_enabled_github_oauth_should_return_correct_github_oauth_url_in_json(
        self, app: Flask, client: FlaskClient
    ):
        setting: Setting = app.config["setting"]
        setting.oauth.google.enable = False
        setting.oauth.github.enable = True
        github_client_id = setting.oauth.github.client_id

        response: TestResponse = client.get("/api/auth/oauth_info")

        response_json: dict[str, str] | None = response.get_json(silent=True)
        assert response_json is not None
        assert (
            response_json["github_oauth_url"]
            == f"https://github.com/login/oauth/authorize?client_id={github_client_id}&scope=repo"
        )
        assert "google_oauth_url" not in response_json

    def test_with_only_enabled_google_oauth_should_return_correct_google_oauth_url_in_json(
        self, app: Flask, client: FlaskClient
    ):
        setting: Setting = app.config["setting"]
        setting.oauth.google.enable = True
        setting.oauth.github.enable = False
        google_client_id = setting.oauth.google.client_id
        google_redirect_url = setting.oauth.google.redirect_url
        google_oauth_scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"

        response: TestResponse = client.get("/api/auth/oauth_info")

        response_json: dict[str, str] | None = response.get_json(silent=True)
        assert response_json is not None
        assert (
            response_json["google_oauth_url"]
            == f"https://accounts.google.com/o/oauth2/v2/auth?client_id={google_client_id}&redirect_uri={google_redirect_url}&response_type=code&scope={google_oauth_scope}"
        )
        assert "github_oauth_url" not in response_json


class TestVertifyMailRoute:
    def test_with_valid_code_should_respond_http_status_ok(
        self, app: Flask, logged_in_client: FlaskClient
    ):
        mail_verification_codes: dict[str, str] = app.config["mail_verification_code"]
        mail_verification_codes |= {"a-random-uuid-here": "test_account"}

        response: TestResponse = logged_in_client.post(
            "/api/auth/verify_mail?code=a-random-uuid-here"
        )

        assert response.status_code == HTTPStatus.OK

    def test_with_valid_code_should_set_user_mail_verify_status_to_true(
        self, app: Flask, logged_in_client: FlaskClient
    ):
        mail_verification_codes: dict[str, str] = app.config["mail_verification_code"]
        mail_verification_codes |= {"a-random-uuid-here": "test_account"}

        logged_in_client.post("/api/auth/verify_mail?code=a-random-uuid-here")

        with app.app_context():
            user: User | None = User.query.filter(User.handle == "test_account").first()
            assert user is not None
            assert user.email_verified == 1

    def test_with_absent_jwt_cookie_should_respond_http_status_forbidden(
        self, client: FlaskClient
    ):
        response: TestResponse = client.post(
            "/api/auth/verify_mail?code=a-random-uuid-here"
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        json_response: dict[str, str] | None = response.get_json(silent=True)
        assert json_response is not None
        assert json_response["message"] == "JWT is not exists."

    def test_with_invalid_jwt_cookie_should_respond_http_status_forbidden(
        self, client: FlaskClient
    ):
        client.set_cookie("", "jwt", "some.invalid.jwt")

        response: TestResponse = client.post(
            "/api/auth/verify_mail?code=a-random-uuid-here"
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_absent_code_should_respond_http_status_forbidden(
        self, logged_in_client: FlaskClient
    ):
        response: TestResponse = logged_in_client.post("/api/auth/verify_mail")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        json_response: dict[str, str] | None = response.get_json(silent=True)
        assert json_response is not None
        assert json_response["message"] == "Absent code."

    def test_with_invalid_code_should_respond_http_status_forbidden(
        self, logged_in_client: FlaskClient
    ):
        response: TestResponse = logged_in_client.post(
            "/api/auth/verify_mail?code=invalid-code"
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        json_response: dict[str, str] | None = response.get_json(silent=True)
        assert json_response is not None
        assert json_response["message"] == "Invalid code."

    def test_with_not_match_handle_and_code_should_respond_http_status_forbidden(
        self, app: Flask, logged_in_client: FlaskClient
    ):
        mail_verification_codes: dict[str, str] = app.config["mail_verification_code"]
        mail_verification_codes |= {"a-random-uuid-here": "some_body"}

        response: TestResponse = logged_in_client.post(
            "/api/auth/verify_mail?code=a-random-uuid-here"
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        json_response: dict[str, str] | None = response.get_json(silent=True)
        assert json_response is not None
        assert json_response["message"] == "Code and handle is not match."


class TestSetupHandleRoute:
    @pytest.fixture()
    def setup_no_handle_user(self, app: Flask) -> None:
        with app.app_context():
            user: User = User(
                user_uid="335cc4aa-23b2-473d-b065-ba51fbbf4f04",
                handle=None,
                password="password-does-not-matter",
                email="no_handle_user@test.com",
                role=1,
                email_verified=1,
            )
            db.session.add(user)
            db.session.commit()

    @pytest.fixture()
    def client_with_hs_cookie(self, app: Flask) -> FlaskClient:
        client: FlaskClient = app.test_client()
        codec: HS256JWTCodec = HS256JWTCodec(app.config["jwt_key"])

        hs_cookie: str = codec.encode({"email": "no_handle_user@test.com"})
        client.set_cookie("", "hs", hs_cookie)

        return client

    def test_with_no_handle_user_should_respond_http_status_ok(
        self, client_with_hs_cookie: FlaskClient, setup_no_handle_user: None
    ):
        payload: dict[str, str] = {"handle": "test_handle"}

        response: TestResponse = client_with_hs_cookie.post(
            "/api/auth/setup_handle", json=payload
        )

        assert response.status_code == HTTPStatus.OK

    def test_with_no_handle_user_should_setup_handle_to_user(
        self, app: Flask, client_with_hs_cookie: FlaskClient, setup_no_handle_user: None
    ):
        payload: dict[str, str] = {"handle": "test_handle"}

        response: TestResponse = client_with_hs_cookie.post(
            "/api/auth/setup_handle", json=payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            user: User | None = User.query.filter(
                User.email == "no_handle_user@test.com"
            ).first()
            assert user is not None
            assert user.handle == "test_handle"

    def test_with_no_hs_cookie_should_respond_http_status_unauthroized(
        self, app: Flask, client: FlaskClient, setup_no_handle_user: None
    ):
        payload: dict[str, str] = {"handle": "test_handle"}

        response: TestResponse = client.post("/api/auth/setup_handle", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json is not None
        assert response.json["message"] == "HS cookie is not exists."

    def test_with_invalid_hs_cookie_should_respond_http_status_unauthroized(
        self, app: Flask, client: FlaskClient, setup_no_handle_user: None
    ):
        payload: dict[str, str] = {"handle": "test_handle"}
        client.set_cookie("", "hs", "invalid_cookie")

        response: TestResponse = client.post("/api/auth/setup_handle", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json is not None
        assert response.json["message"] == "HS cookie is invalid."

    def test_with_bad_format_payload_should_respond_http_status_bad_request(
        self, app: Flask, client_with_hs_cookie: FlaskClient, setup_no_handle_user: None
    ):
        payload: dict[str, str] = {"bad": "payload"}

        response: TestResponse = client_with_hs_cookie.post(
            "/api/auth/setup_handle", json=payload
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json is not None
        assert response.json["message"] == "Wrong payload format."

    def test_with_invalid_handle_should_respond_http_status_unprocessable_entity(
        self, app: Flask, client_with_hs_cookie: FlaskClient, setup_no_handle_user: None
    ):
        payload: dict[str, str] = {"handle": "-invalid-handle"}

        response: TestResponse = client_with_hs_cookie.post(
            "/api/auth/setup_handle", json=payload
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json is not None
        assert response.json["message"] == "Handle is invalid."

    def test_with_repeated_handle_should_respond_http_status_forbidden(
        self,
        app: Flask,
        client_with_hs_cookie: FlaskClient,
        setup_no_handle_user: None,
        setup_test_user: None,
    ):
        payload: dict[str, str] = {"handle": "nuoj"}

        response: TestResponse = client_with_hs_cookie.post(
            "/api/auth/setup_handle", json=payload
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json is not None
        assert response.json["message"] == "Handle is repeated."


def _get_cookies(cookie_jar: CookieJar | None) -> tuple[Cookie, ...]:
    if cookie_jar is None:
        return tuple()
    return tuple(cookie for cookie in cookie_jar)


def _verify_data_field_in_cookie_payload(
    codec: HS256JWTCodec, cookie_jar, cookie_name: str, payload: dict[str, str]
) -> bool:
    cookies: tuple[Cookie, ...] = _get_cookies(cookie_jar)
    (jwt_cookie,) = tuple(filter(lambda x: x.name == cookie_name, cookies))
    assert jwt_cookie.value is not None
    jwt_payload: dict[str, Any] = codec.decode(jwt_cookie.value)
    return payload == jwt_payload["data"]
