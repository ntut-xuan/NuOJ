import json
import requests
from typing import Final

from flask import current_app

from api.auth.oauth_util import OAuthLoginResult, _init_oauth_user_data_and_profile_if_user_not_exists
from setting.util import Setting


ACCESS_TOKEN_URL: Final[str] = "https://oauth2.googleapis.com/token"
USER_PROFILE_API_URL: Final[str] = "https://www.googleapis.com/oauth2/v2/userinfo"


def google_login(code) -> bool:
    
    access_token: str | None = _get_access_token_from_code(code)
    
    if access_token is None:
        return OAuthLoginResult(None, False)
    
    email = _get_user_email_from_access_token(access_token)

    _init_oauth_user_data_and_profile_if_user_not_exists(email)

    return OAuthLoginResult(email, True)


def _get_access_token_from_code(code: str) -> str:
    setting: Setting = current_app.config.get("setting")
    client_id = setting.google_oauth_client_id()
    client_secret = setting.google_oauth_secret()
    redirect_uri = setting.google_oauth_redirect_url()

    payload = {
        "code": code, 
        "client_id": client_id, 
        "client_secret": client_secret, 
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    
    headers = {
        "content-type": "application/json"
    }

    response: requests.Response = requests.post(ACCESS_TOKEN_URL, data=json.dumps(payload), headers=headers)
    response_json = json.loads(response.text)
    
    if "access_token" not in response_json:
        return None
    
    access_token = response_json["access_token"]
    
    return access_token


def _get_user_email_from_access_token(access_token: str) -> str:
    response = requests.get(USER_PROFILE_API_URL, params={"access_token": access_token})
    response_json = json.loads(response.text)
    
    assert "email" in response_json

    email = response_json["email"]
    return email