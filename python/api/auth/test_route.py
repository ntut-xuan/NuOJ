from http import HTTPStatus

from flask import Blueprint, request, make_response

auth_test_bp = Blueprint("auth_test", __name__, url_prefix="/test")


@auth_test_bp.route("/github/access_token", methods=["POST"])
def access_token_test_route():
    code: str | None = request.args.get("code", None)
    
    assert code is not None
    
    if code == "valid_code":
        return make_response({"message": "OK", "access_token": "valid_access_token"})
    else:
        return make_response({"error": "Invalid Code"}, HTTPStatus.FORBIDDEN)


@auth_test_bp.route("/github/user_profile", methods=["GET"])
def oauth_user_profile_test_route():
    authorization_header: str | None = request.headers.get("Authorization", None)
    
    assert authorization_header is not None
    
    if authorization_header == "token valid_access_token":
        return make_response({"login": "oauth_test", "email": "oauth_test@nuoj.com"})