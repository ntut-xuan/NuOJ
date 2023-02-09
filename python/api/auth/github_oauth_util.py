#!/usr/bin/env python3
import json
from requests import Response, get, post
from dataclasses import dataclass
from typing import Any

from api.auth.oauth_util import OAuthLoginResult, _init_oauth_user_data_and_profile_if_user_not_exists
from setting_util import github_oauth_client_id, github_oauth_secret


@dataclass
class UserProfile:
    username: str
    email: str


def github_login(code) -> OAuthLoginResult:

    client_id = github_oauth_client_id()
    client_secret = github_oauth_secret()
    
    access_token: str | None = _validate_github_oauth_code_and_get_access_token(client_id, client_secret, code)

    if access_token is None:
        return OAuthLoginResult(None, False)

    user_profile: UserProfile = _get_user_email_with_access_token(access_token)

    _init_oauth_user_data_and_profile_if_user_not_exists(user_profile.email)

    return OAuthLoginResult(user_profile.email, True)


def _validate_github_oauth_code_and_get_access_token(client_id: str, client_secret: str, code: str) -> str | None:
    parameters: dict[str, str] = {"client_id": client_id, "client_secret": client_secret, "code": code}
    headers: dict[str, str] = {"Accept": "application/json"}
    response: Response = post("https://github.com/login/oauth/access_token", params=parameters, headers=headers)
    
    response_json: dict[str, Any] = json.loads(response.text)
    
    if "access_token" not in response_json:
        return None
    
    return response_json["access_token"]


def _get_user_email_with_access_token(access_token: str) -> str:
    headers: dict[str, str] = {
        "Accept": "application/json",
        "Authorization": f"token {access_token}"
    }
    response: Response = get("https://api.github.com/user", headers=headers)
    
    response_json: dict[str, Any] = json.loads(response.text)
    
    assert response_json is not None
    
    username: str = response_json["login"]
    email: str = response_json.get("email", username + "@github.com")
    
    return email