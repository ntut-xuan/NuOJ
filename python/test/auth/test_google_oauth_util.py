import pytest
from flask import Flask

import api.auth.google_oauth_util
from api.auth.oauth_util import OAuthLoginResult
from api.auth.google_oauth_util import (
    google_login,
    _get_access_token_from_code,
    _get_user_email_from_access_token,
)
from database_util import TunnelCode, file_storage_tunnel_exist
from models import Profile, User


def test_mock_access_token_url_should_change_the_access_token_url(
    app: Flask, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(
        api.auth.google_oauth_util, "ACCESS_TOKEN_URL", "some_random_url"
    )

    assert api.auth.google_oauth_util.ACCESS_TOKEN_URL == "some_random_url"


def test_mock_user_profile_url_should_change_the_user_profile_url(
    app: Flask, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(
        api.auth.google_oauth_util, "USER_PROFILE_API_URL", "some_random_url"
    )

    assert api.auth.google_oauth_util.USER_PROFILE_API_URL == "some_random_url"


def test_validate_code_with_valid_oauth_code_should_return_valid_access_token(
    app: Flask, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(
        api.auth.google_oauth_util,
        "ACCESS_TOKEN_URL",
        "http://0.0.0.0:8080/test/google/access_token",
    )

    with app.app_context():
        access_token: str | None = _get_access_token_from_code("valid_code")
        assert access_token == "valid_access_token"


def test_get_user_email_with_valid_access_token_should_return_email(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        api.auth.google_oauth_util,
        "USER_PROFILE_API_URL",
        "http://0.0.0.0:8080/test/google/user_profile",
    )

    access_token: str | None = _get_user_email_from_access_token("valid_access_token")
    assert access_token == "oauth_test@nuoj.com"


class TestGoogleOAuthWithMOCK:
    def test_google_login_with_valid_code_should_passed_the_verify(
        self, app: Flask, monkeypatch: pytest.MonkeyPatch
    ):
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
        with app.app_context():
            result: OAuthLoginResult = google_login("valid_code")

            assert result.passed

    def test_google_login_with_valid_code_should_have_correct_user_email(
        self, app: Flask, monkeypatch: pytest.MonkeyPatch
    ):
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
        with app.app_context():
            result: OAuthLoginResult = google_login("valid_code")

            assert result.email == "oauth_test@nuoj.com"

    def test_google_login_with_valid_code_and_new_email_should_init_the_user_data(
        self, app: Flask, monkeypatch: pytest.MonkeyPatch
    ):
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
        with app.app_context():
            result: OAuthLoginResult = google_login("valid_code")

            user: User | None = User.query.filter(User.email == result.email).first()
            profile: Profile | None = Profile.query.filter(
                Profile.user_uid == user.user_uid
            ).first()
            assert user is not None
            assert profile is not None

    def test_google_login_with_valid_code_and_new_email_should_init_the_user_profile_in_storage(
        self, app: Flask, monkeypatch: pytest.MonkeyPatch
    ):
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
        with app.app_context():
            result: OAuthLoginResult = google_login("valid_code")

            user: User | None = User.query.filter(User.email == result.email).first()
            assert file_storage_tunnel_exist(
                f"{user.user_uid}.json", TunnelCode.USER_PROFILE
            )

    def test_google_login_with_invalid_code_should_fail_the_verify(
        self, app: Flask, monkeypatch: pytest.MonkeyPatch
    ):
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
        with app.app_context():
            result: OAuthLoginResult = google_login("invalid_code")

            assert not result.passed
