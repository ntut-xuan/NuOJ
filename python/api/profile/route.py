import io
from http import HTTPStatus

from flask import Blueprint, Response, make_response, request, send_file
from PIL import Image

from api.auth.validator import (
    validate_jwt_is_exists_or_return_unauthorized,
    validate_jwt_is_valid_or_return_unauthorized
)
from api.profile.validator import (
    operator_should_be_owner_or_return_http_status_forbidden,
    payload_should_have_correct_format_or_return_http_status_bad_request,
    user_should_exists_or_return_http_status_forbidden,
    validate_image_or_return_bad_request,
)
from database import db
from models import Profile, User
from storage.util import TunnelCode, is_file_exists, read_file_bytes, write_file_bytes
from util import make_simple_error_response

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.route("/<string:name>", methods=["GET"])
@user_should_exists_or_return_http_status_forbidden
def fetch_profile(name: str) -> Response:
    user: User = _get_user_by_name(name)
    profile: Profile = _get_profile_by_name(name)

    payload: dict[str, str] = {
        "user_uid": profile.user_uid,
        "email": profile.email,
        "school": profile.school,
        "bio": profile.bio,
        "handle": user.handle,
        "role": user.role
    }

    return make_response(payload)

@profile_bp.route("/<string:name>", methods=["PUT"])
@user_should_exists_or_return_http_status_forbidden
@payload_should_have_correct_format_or_return_http_status_bad_request
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
@operator_should_be_owner_or_return_http_status_forbidden
def update_profile(name: str) -> Response:
    profile: Profile = _get_profile_by_name(name)
    payload: dict[str, str] | None = request.get_json(silent=True)

    assert payload is not None

    for key, value in payload.items():
        setattr(profile, key, value)
    
    db.session.commit()
    return make_response({"message": "OK"})


@profile_bp.route("/<string:name>/avatar", methods=["GET"])
@user_should_exists_or_return_http_status_forbidden
def fetch_profile_avatar(name: str):
    profile: Profile = _get_profile_by_name(name)
    user_uid: str = profile.user_uid

    img_type: str = profile.img_type
    img_binaries: bytes = read_file_bytes(
        f"{user_uid}.{img_type}", TunnelCode.USER_AVATER
    )

    return send_file(
        io.BytesIO(img_binaries),
        download_name=f"{user_uid}.{img_type}",
        mimetype="image/png"
    )

@profile_bp.route("/<string:name>/avatar", methods=["PUT"])
@validate_jwt_is_exists_or_return_unauthorized
@validate_jwt_is_valid_or_return_unauthorized
@user_should_exists_or_return_http_status_forbidden
@validate_image_or_return_bad_request
@operator_should_be_owner_or_return_http_status_forbidden
def upload_profile_avatar(name: str):
    image_data: bytes = request.data
    profile: Profile = _get_profile_by_name(name)
    user_uid: str = profile.user_uid

    image: Image = Image.open(io.BytesIO(image_data))
    image_binary = io.BytesIO()
    image.save(image_binary, format='PNG')
    
    write_file_bytes(f"{user_uid}.png", image_binary.getvalue(), TunnelCode.USER_AVATER)
    return make_response({"message": "OK"})


def _get_user_by_name(name: str) -> User:
    user: User | None = User.query.filter_by(handle=name).first()
    assert user is not None

    return user


def _get_profile_by_name(name: str) -> Profile:
    user: User = _get_user_by_name(name)
    profile: Profile | None = Profile.query.filter_by(user_uid=user.user_uid).first()
    assert profile is not None

    return profile
