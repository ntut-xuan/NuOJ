import json
import jwt
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Any

from flask import Blueprint, Response, current_app, request, make_response, send_from_directory
from sqlalchemy.sql import or_

import setting_util
from api.auth.auth_util import HS256JWTCodec, LoginPayload, login, register
from api.auth.validator import (
    validate_email_or_return_unprocessable_entity,
    validate_email_is_not_repeated_or_return_forbidden,
    validate_login_payload_format_or_return_bad_request,
    validate_handle_or_return_unprocessable_entity,
    validate_handle_is_not_repeated_or_return_forbidden,
    validate_password_or_return_unprocessable_entity,
    validate_register_payload_format_or_return_bad_request,
)
from models import User
from util import make_simple_error_response

auth = Blueprint('auth', __name__, url_prefix="/api")

@auth.route("/login", methods=["POST"])
@validate_login_payload_format_or_return_bad_request
def login_route():
    payload: dict[str, Any] | None = request.get_json(silent=True)
    login_payload: LoginPayload = LoginPayload(**payload)
    
    if not login(login_payload.account, login_payload.password):
        return make_simple_error_response(HTTPStatus.FORBIDDEN, "Incorrect account or password")
    
    response: Response = make_response({"message": "OK"}, HTTPStatus.OK)
    user: User = _get_user_info_from_account(login_payload.account)
    _set_jwt_cookie_to_response({"email": user.email, "handle": user.handle}, response)
    
    return response


@auth.route("/register", methods=["POST"])
@validate_register_payload_format_or_return_bad_request
@validate_email_or_return_unprocessable_entity
@validate_handle_or_return_unprocessable_entity
@validate_password_or_return_unprocessable_entity
@validate_email_is_not_repeated_or_return_forbidden
@validate_handle_is_not_repeated_or_return_forbidden
def register_route():
    payload: dict[str, Any] | None = request.get_json(silent=True)
    email: str = payload["email"]
    handle: str = payload["handle"]
    password: str = payload["password"]

    register(email, handle, password)

    # if result["status"] == "Failed":
    #     return Response(json.dumps(result), mimetype="application/json")

    # if setting_util.mail_verification_enable():
    #     verification_code = result["verification_code"]
    #     result["mail_verification_redirect"] = True
    #     del result["verification_code"]
    # else:
    #     result["mail_verification_redirect"] = False

    # resp = Response(json.dumps(result), mimetype="application/json")

    # if setting_util.mail_verification_enable() == False:
    #     sessionID = payload_generator(result["data"]["handle"], result["data"]["email"])
    #     resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
    # else:
    #     verification_code_dict[verification_code] = result["data"]["handle"]

    response: Response = make_response({"message": "OK"}, HTTPStatus.OK)
    return response


@auth.route("/oauth_info", methods=["GET"])
def oauth_info():
    github_status = setting_util.github_oauth_enable()
    google_status = setting_util.github_oauth_enable()
    github_client_id = setting_util.github_oauth_client_id()
    google_client_id = setting_util.google_oauth_client_id()
    google_redirect_url = setting_util.google_oauth_redirect_url()
    google_oauth_scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"

    response = {"status": "OK"}

    if github_status:
        response["github_oauth_url"] = "https://github.com/login/oauth/authorize?client_id=%s&scope=repo" % (github_client_id)

    if google_status:
        response["google_oauth_url"] = "https://accounts.google.com/o/oauth2/v2/auth?client_id=%s&redirect_uri=%s&response_type=code&scope=%s" % (google_client_id, google_redirect_url, google_oauth_scope)

    return Response(json.dumps(response), mimetype="application/json")

@auth.route("/pubkey")
def pubkey():
	return send_from_directory('../', "public.pem")


def _get_user_info_from_account(account: str) -> User:
    user: User | None = User.query.filter(or_(User.email == account, User.handle == account)).first()
    
    assert user is not None
    
    return user

def _generate_ok_response_with_jwt(username, email):
    response: Response = make_response({"message": "OK"}, HTTPStatus.OK)
    expired_time: datetime = datetime.now(tz=timezone.utc) + timedelta(days=1)
    jwt_payload: dict[str, Any] = {"handle": username, "email": email, "iat": datetime.now(tz=timezone.utc), "exp": expired_time}
    jwt_token: str = jwt.encode(jwt_payload, "secret", algorithm="HS256")
    
    response.set_cookie(key="jwt", value=jwt_token, expires=expired_time)

    return response

def _set_jwt_cookie_to_response(
    payload: dict[str, Any],
    response: Response,
    expiration_time_delta: timedelta = timedelta(days=1),
) -> None:
    codec = HS256JWTCodec(current_app.config["jwt_key"])
    token: str = codec.encode(payload, expiration_time_delta)
    response.set_cookie(
        "jwt",
        value=token,
        expires=datetime.now(tz=timezone.utc) + expiration_time_delta,
    )
