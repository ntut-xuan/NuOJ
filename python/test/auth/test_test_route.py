from http import HTTPStatus

import pytest

from flask import Flask
from werkzeug.test import TestResponse

class TestGithubTestRoute:
    def test_github_access_token_test_route_with_valid_code_should_respond_http_status_ok(self, client: Flask):
        response: TestResponse = client.post("/test/github/access_token?code=valid_code")
        
        assert response.status_code == HTTPStatus.OK

    def test_github_access_token_test_route_with_valid_code_should_respond_valid_access_token(self, client: Flask):
        response: TestResponse = client.post("/test/github/access_token?code=valid_code")
        
        assert response.status_code == HTTPStatus.OK
        assert response.json is not None
        assert response.json["access_token"] == "valid_access_token"

    def test_github_access_token_test_route_with_invalid_code_should_respond_http_status_forbidden(self, client: Flask):
        response: TestResponse = client.post("/test/github/access_token?code=invalid_code")
        
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_github_user_profile_test_route_with_valid_access_token_should_respond_http_status_ok(self, client: Flask):
        response: TestResponse = client.get("/test/github/user_profile", headers={"Authorization": "token valid_access_token"})
        
        assert response.status_code == HTTPStatus.OK
        
    def test_github_user_profile_test_route_with_valid_access_token_should_respond_correct_payload(self, client: Flask):
        response: TestResponse = client.get("/test/github/user_profile", headers={"Authorization": "token valid_access_token"})
        
        assert response.status_code == HTTPStatus.OK
        assert response.json is not None
        assert response.json["login"] == "oauth_test"
        assert response.json["email"] == "oauth_test@nuoj.com"
        
class TestGoogleTestRoute:
    def _get_payload(self, valid: bool):
        payload = {
            "code": "valid_code" if valid else "invalid_code", 
            "client_id": "some_client_id", 
            "client_secret": "some_client_secret", 
            "redirect_uri": "some_redirect_uri",
            "grant_type": "authorization_code"
        }
        return payload

    def test_google_access_token_test_route_with_valid_code_should_respond_http_status_ok(self, client: Flask):
        response: TestResponse = client.post("/test/google/access_token", json=self._get_payload(True))
        
        assert response.status_code == HTTPStatus.OK

    def test_google_access_token_test_route_with_valid_code_should_respond_valid_access_token(self, client: Flask):
        response: TestResponse = client.post("/test/google/access_token", json=self._get_payload(True))
        
        assert response.status_code == HTTPStatus.OK
        assert response.json is not None
        assert response.json["access_token"] == "valid_access_token"

    def test_google_access_token_test_route_with_invalid_code_should_respond_http_status_forbidden(self, client: Flask):
        response: TestResponse = client.post("/test/google/access_token", json=self._get_payload(False))
        
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_google_user_profile_test_route_with_valid_access_token_should_respond_http_status_ok(self, client: Flask):
        response: TestResponse = client.get("/test/google/user_profile?access_token=valid_access_token")
        
        assert response.status_code == HTTPStatus.OK
        
    def test_google_user_profile_test_route_with_valid_access_token_should_respond_correct_payload(self, client: Flask):
        response: TestResponse = client.get("/test/google/user_profile?access_token=valid_access_token")
        
        assert response.status_code == HTTPStatus.OK
        assert response.json is not None
        assert response.json["email"] == "oauth_test@nuoj.com"