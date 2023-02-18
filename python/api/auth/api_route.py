import json
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Any

from flask import Blueprint, Response, current_app, request, make_response, redirect
from sqlalchemy.sql import or_

from api.auth.auth_util import (
    HS256JWTCodec,
    LoginPayload,
    login,
    register,
    setup_handle,
    verified_the_email_of_handle,
)
from api.auth.github_oauth_util import github_login
from api.auth.google_oauth_util import google_login
from api.auth.oauth_util import OAuthLoginResult
from api.auth.validator import (
    validate_email_or_return_unprocessable_entity,
    validate_email_is_not_repeated_or_return_forbidden,
    validate_jwt_is_exists_or_return_unauthorized,
    validate_jwt_is_valid_or_return_unauthorized,
    validate_login_payload_format_or_return_bad_request,
    validate_handle_or_return_unprocessable_entity,
    validate_handle_is_not_repeated_or_return_forbidden,
    validate_hs_cookie_is_exists_or_return_unauthorized,
    validate_hs_cookie_is_valid_or_return_unauthorized,
    validate_password_or_return_unprocessable_entity,
    validate_register_payload_format_or_return_bad_request,
    validate_setup_handle_payload_format_or_return_bad_request,
)
from setting.util import Setting
from models import User
from util import make_simple_error_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
@validate_login_payload_format_or_return_bad_request
def login_route():
    payload: dict[str, Any] | None = request.get_json(silent=True)
    login_payload: LoginPayload = LoginPayload(**payload)

    if not login(login_payload.account, login_payload.password):
        return make_simple_error_response(
            HTTPStatus.FORBIDDEN, "Incorrect account or password"
        )

    user: User = _get_user_info_from_account(login_payload.account)
    setting: Setting = current_app.config.get("setting")

    if setting.mail.enable and user.email_verified == 0:
        return make_simple_error_response(
            HTTPStatus.UNAUTHORIZED, "Mail verification enabled but mail is not verify."
        )

    response: Response = make_response({"message": "OK"}, HTTPStatus.OK)
    _set_cookie_to_response(
        "jwt", {"email": user.email, "handle": user.handle}, response
    )
    return response


@auth_bp.route("/register", methods=["POST"])
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

    setting: Setting = current_app.config.get("setting")
    mail_verification_enabled = setting.mail.enable
    response: Response = make_response(
        {"message": "OK", "mail_verification_enabled": mail_verification_enabled},
        HTTPStatus.OK,
    )
    return response


@auth_bp.route("/oauth_info", methods=["GET"])
def oauth_info_route():
    current_setting: Setting = current_app.config.get("setting")

    github_status = current_setting.oauth.github.enable
    google_status = current_setting.oauth.google.enable
    github_client_id = current_setting.oauth.github.client_id
    google_client_id = current_setting.oauth.google.client_id
    google_redirect_url = current_setting.oauth.google.redirect_url
    google_oauth_scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"

    response = {"status": "OK"}

    if github_status:
        response[
            "github_oauth_url"
        ] = f"https://github.com/login/oauth/authorize?client_id={github_client_id}&scope=repo"

    if google_status:
        response[
            "google_oauth_url"
        ] = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={google_client_id}&redirect_uri={google_redirect_url}&response_type=code&scope={google_oauth_scope}"

    return Response(json.dumps(response), mimetype="application/json")


# @auth.route("/pubkey")
# def pubkey():
# 	return send_from_directory('../', "public.pem")


@auth_bp.route("/verify_jwt", methods=["POST"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
def verify_jwt_route() -> Response:
    response: Response = make_response({"message": "OK"}, HTTPStatus.OK)
    return response


@auth_bp.route("/github_login", methods=["GET"])
def github_login_route():
    code: str = request.args.get("code")
    oauth_login_result: OAuthLoginResult = github_login(code)

    response: Response

    if oauth_login_result.passed:
        user: User = _get_user_info_from_account(oauth_login_result.email)
        if user.handle is None:
            response = redirect("/handle_setup")
        else:
            response = redirect("/")
            _set_cookie_to_response(
                "jwt", {"email": user.email, "handle": user.handle}, response
            )
    else:
        response = make_simple_error_response(
            HTTPStatus.FORBIDDEN, "Github OAuth login failed."
        )
    return response


@auth_bp.route("/google_login", methods=["GET"])
def google_login_route():
    code: str = request.args.get("code")
    error: str | None = request.args.get("error")

    if error is not None:
        make_simple_error_response(
            HTTPStatus.FORBIDDEN,
            "Google OAuth login failed since args have error argument.",
        )

    oauth_login_result: OAuthLoginResult = google_login(code)

    response: Response

    if oauth_login_result.passed:
        user: User = _get_user_info_from_account(oauth_login_result.email)
        if user.handle is None:
            response = redirect("/handle_setup")
            _set_cookie_to_response("hs", {"email": user.email}, response)
        else:
            response = redirect("/")
            _set_cookie_to_response(
                "jwt", {"email": user.email, "handle": user.handle}, response
            )
    else:
        response = make_simple_error_response(
            HTTPStatus.FORBIDDEN, "Google OAuth login failed."
        )
    return response


@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    resp: Response = Response(json.dumps({"status": "OK"}))
    resp.set_cookie("jwt", value="", expires=0)
    return resp


@auth_bp.route("/verify_mail", methods=["POST"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
def verify_mail_route():
    mail_verification_codes: dict[str, str] = current_app.config.get(
        "mail_verification_code"
    )

    code: str | None = request.args.get("code", None)

    if code is None:
        return make_simple_error_response(HTTPStatus.BAD_REQUEST, "Absent code.")

    if code not in mail_verification_codes:
        return make_simple_error_response(
            HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid code."
        )

    jwt_token: str = request.cookies.get("jwt")
    codec: HS256JWTCodec = HS256JWTCodec(current_app.config.get("jwt_key"))
    jwt_payload: dict[str, str] = codec.decode(jwt_token)
    handle: str = jwt_payload["data"]["handle"]

    if handle != mail_verification_codes[code]:
        return make_simple_error_response(
            HTTPStatus.FORBIDDEN, "Code and handle is not match."
        )

    del mail_verification_codes[code]
    verified_the_email_of_handle(handle)
    return make_response({"message": "OK"}, HTTPStatus.OK)


@auth_bp.route("/setup_handle", methods=["POST"])
@validate_hs_cookie_is_exists_or_return_unauthorized
@validate_hs_cookie_is_valid_or_return_unauthorized
@validate_setup_handle_payload_format_or_return_bad_request
@validate_handle_or_return_unprocessable_entity
@validate_handle_is_not_repeated_or_return_forbidden
def setup_handle_route():
    hs_cookie: str | None = request.cookies.get("hs", None)
    codec: HS256JWTCodec = HS256JWTCodec(current_app.config.get("jwt_key"))

    assert hs_cookie is not None

    hs_payload: dict[str, Any] = codec.decode(hs_cookie)
    payload: dict[str, Any] | None = request.get_json(silent=True)

    assert payload is not None

    email: str | None = hs_payload["data"].get("email", None)
    handle: str = payload.get("handle", None)

    assert email is not None

    setup_handle(email, handle)

    return make_response({"message": "OK"}, HTTPStatus.OK)


def _get_user_info_from_account(account: str) -> User:
    user: User | None = User.query.filter(
        or_(User.email == account, User.handle == account)
    ).first()

    assert user is not None

    return user


def _set_cookie_to_response(
    name: str,
    payload: dict[str, Any],
    response: Response,
    expiration_time_delta: timedelta = timedelta(days=1),
) -> None:
    codec = HS256JWTCodec(current_app.config["jwt_key"])
    token: str = codec.encode(payload, expiration_time_delta)
    response.set_cookie(
        name,
        value=token,
        expires=datetime.now(tz=timezone.utc) + expiration_time_delta,
    )
