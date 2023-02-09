from http import HTTPStatus

import pytest

from flask import Flask
from werkzeug.test import TestResponse

def test_github_access_token_test_route_with_valid_code_should_respond_http_status_ok(client: Flask):
    response: TestResponse = client.post("/test/github/access_token?code=valid_code")
    
    assert response.status_code == HTTPStatus.OK

def test_github_access_token_test_route_with_valid_code_should_respond_valid_access_token(client: Flask):
    response: TestResponse = client.post("/test/github/access_token?code=valid_code")
    
    assert response.status_code == HTTPStatus.OK
    assert response.json is not None
    assert response.json["access_token"] == "valid_access_token"

def test_github_access_token_test_route_with_invalid_code_should_respond_http_status_forbidden(client: Flask):
    response: TestResponse = client.post("/test/github/access_token?code=invalid_code")
    
    assert response.status_code == HTTPStatus.FORBIDDEN

def test_github_user_profile_test_route_with_valid_access_token_should_respond_http_status_ok(client: Flask):
    response: TestResponse = client.get("/test/github/user_profile", headers={"Authorization": "token valid_access_token"})
    
    assert response.status_code == HTTPStatus.OK
    
def test_github_user_profile_test_route_with_valid_access_token_should_respond_correct_payload(client: Flask):
    response: TestResponse = client.get("/test/github/user_profile", headers={"Authorization": "token valid_access_token"})
    
    assert response.status_code == HTTPStatus.OK
    assert response.json is not None
    assert response.json["login"] == "oauth_test"
    assert response.json["email"] == "oauth_test@nuoj.com"