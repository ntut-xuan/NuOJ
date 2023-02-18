#!/usr/bin/env python3
import json
from requests import Response, get, post
from typing import Any, Final

from flask import current_app

from api.auth.oauth_util import (
    OAuthLoginResult,
    _init_oauth_user_data_and_profile_if_user_not_exists,
)
from setting.util import Setting

ACCESS_TOKEN_URL: Final[str] = "https://github.com/login/oauth/access_token"
USER_PROFILE_API_URL: Final[str] = "https://api.github.com/user"


def github_login(code) -> OAuthLoginResult:
    setting: Setting = current_app.config.get("setting")
    client_id = setting.oauth.github.client_id
    client_secret = setting.oauth.github.secret

    access_token: str | None = _validate_github_oauth_code_and_get_access_token(
        client_id, client_secret, code
    )

    if access_token is None:
        return OAuthLoginResult(None, False)

    email: str = _get_user_email_with_access_token(access_token)

    _init_oauth_user_data_and_profile_if_user_not_exists(email)

    return OAuthLoginResult(email, True)


def _validate_github_oauth_code_and_get_access_token(
    client_id: str, client_secret: str, code: str
) -> str | None:
    parameters: dict[str, str] = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }
    headers: dict[str, str] = {"Accept": "application/json"}
    response: Response = post(ACCESS_TOKEN_URL, params=parameters, headers=headers)

    response_json: dict[str, Any] = json.loads(response.text)

    if "access_token" not in response_json:
        return None

    return response_json["access_token"]


def _get_user_email_with_access_token(access_token: str) -> str:
    headers: dict[str, str] = {
        "Accept": "application/json",
        "Authorization": f"token {access_token}",
    }
    response: Response = get(USER_PROFILE_API_URL, headers=headers)

    response_json: dict[str, Any] = json.loads(response.text)

    assert response_json is not None

    username: str = response_json["login"]
    email: str = response_json.get("email", username + "@github.com")

    return email
