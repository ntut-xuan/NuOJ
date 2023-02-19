from http import HTTPStatus

from flask import Blueprint, Response, request, make_response

auth_test_bp = Blueprint("auth_test", __name__, url_prefix="/test")


@auth_test_bp.route("/github/access_token", methods=["POST"])
def github_access_token_test_route() -> Response:
    code: str | None = request.args.get("code", None)

    assert code is not None

    if code == "valid_code":
        return make_response({"message": "OK", "access_token": "valid_access_token"})
    else:
        return make_response({"error": "Invalid Code"}, HTTPStatus.FORBIDDEN)


@auth_test_bp.route("/github/user_profile", methods=["GET"])
def github_oauth_user_profile_test_route() -> Response:
    authorization_header: str | None = request.headers.get("Authorization", None)

    assert authorization_header is not None

    if authorization_header == "token valid_access_token":
        return make_response({"login": "oauth_test", "email": "oauth_test@nuoj.com"})
    else:
        return make_response({"error": "Invalid access token"}, HTTPStatus.FORBIDDEN)


@auth_test_bp.route("/google/access_token", methods=["POST"])
def google_access_token_test_route() -> Response:
    request_payload: dict[str, str] | None = request.get_json(silent=True)

    assert request_payload is not None
    assert "code" in request_payload

    code: str = request_payload["code"]

    if code == "valid_code":
        return make_response({"message": "OK", "access_token": "valid_access_token"})
    else:
        return make_response({"error": "Invalid Code"}, HTTPStatus.FORBIDDEN)


@auth_test_bp.route("/google/user_profile", methods=["GET"])
def google_oauth_user_profile_test_route() -> Response:
    access_token: str | None = request.args.get("access_token")

    assert access_token is not None

    if access_token == "valid_access_token":
        return make_response({"email": "oauth_test@nuoj.com"})
    else:
        return make_response({"error": "Invalid access token"}, HTTPStatus.FORBIDDEN)
