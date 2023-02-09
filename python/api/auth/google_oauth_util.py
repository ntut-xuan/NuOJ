from flask import *
import json
import requests

from api.auth.oauth_util import OAuthLoginResult, _init_oauth_user_data_and_profile_if_user_not_exists
from setting_util import google_oauth_client_id, google_oauth_secret, google_oauth_redirect_url


def google_login(code) -> bool:
    
    access_token: str | None = _get_access_token_from_code(code)
    
    if access_token is None:
        return OAuthLoginResult(None, False)
    
    email = _get_user_email_from_access_token(access_token)

    _init_oauth_user_data_and_profile_if_user_not_exists(email)

    return OAuthLoginResult(email, True)


def _get_access_token_from_code(code: str) -> str:
    client_id = google_oauth_client_id()
    client_secret = google_oauth_secret()
    redirect_uri = google_oauth_redirect_url()

    payload = {
        "code": code, 
        "client_id": client_id, 
        "client_secret": client_secret, 
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    response: requests.Response = requests.post("https://oauth2.googleapis.com/token", data=payload)
    response_json = json.loads(response.text)
    
    print(response_json)
    
    if "access_token" not in response_json:
        return None
    
    access_token = response_json["access_token"]
    
    return access_token


def _get_user_email_from_access_token(access_token: str) -> str:
    response = requests.get(f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}")
    response_json = json.loads(response.text)
    
    assert "email" in response_json

    email = response_json["email"]
    return email