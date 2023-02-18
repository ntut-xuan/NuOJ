#!/usr/bin/env python3
from flask import *
import json
import hashlib
import threading
import jwt
import database_util
import crypto_util as crypto_util
from datetime import *
from tunnel_code import TunnelCode
from uuid import uuid4

from typing import Any, Final
from dataclasses import dataclass

from sqlalchemy.sql import or_, and_

from api.auth.email_util import send_verification_email
from database import db
from models import User, Profile
from setting.util import Setting


@dataclass
class LoginPayload:
    account: str
    password: str


@dataclass
class RegisterPayload:
    email: str
    handle: str
    password: str


@dataclass
class SetupHandlePayload:
    handle: str


def hash_password(password) -> str:
    m = hashlib.sha256()
    m.update(password.encode("utf8"))
    password = m.hexdigest()
    return password


def login(account: str, password: str) -> bool:
    password = hash_password(password)

    user: User | None = User.query.filter(
        and_(
            or_(User.email == account, User.handle == account),
            User.password == password,
        )
    ).first()

    if user == None:
        return False

    return True


def register(email: str, handle: str, password: str) -> None:
    # password = crypto_util.Decrypt(password)
    # response = {"status": "OK"}

    # Hash
    password = hash_password(password)

    # Create user_uid
    user_uid = str(uuid4())

    _init_user_data_to_database(user_uid, password, handle, email)

    # Write into storage (init)
    assert not _is_profile_storage_exist(user_uid)
    _init_profile_storage_file(user_uid, handle, email)

    # Send the email if the email verification is enabled.
    setting: Setting = current_app.config.get("setting")
    if setting.mail.enable:
        thread = FlaskThread(target=send_verification_email, args=[handle, email])
        thread.start()


def setup_handle(account, handle) -> None:
    # Setup Handle
    user: User | None = User.query.filter(User.email == account).first()
    assert user is not None

    user.handle = handle
    db.session.commit()

    # Setup Handle on storage data
    _init_profile_storage_file(user.user_uid, user.handle, user.email)


def is_user_already_have_handle(email: str) -> bool:
    user: User | None = User.query.filter(User.email == email).first()
    assert user is not None

    return user.handle is not None


def verified_the_email_of_handle(handle: str) -> None:
    user: User | None = User.query.filter(User.handle == handle).first()
    assert user is not None

    user.email_verified = 1
    db.session.commit()


def _init_profile_storage_file(user_uid: str, handle: str, email: str) -> None:
    database_util.file_storage_tunnel_write(
        user_uid + ".json",
        json.dumps({"handle": handle, "email": email, "school": "", "bio": ""}),
        TunnelCode.USER_PROFILE,
    )


def _is_profile_storage_exist(user_uid: str) -> bool:
    return database_util.file_storage_tunnel_exist(
        user_uid + ".json", TunnelCode.USER_PROFILE
    )


def _init_user_data_to_database(
    user_uid: str,
    password: str,
    handle: str,
    email: str,
    role: int = 0,
    email_verified: int = 0,
):
    user: User = User(
        user_uid=user_uid,
        handle=handle,
        password=password,
        email=email,
        role=role,
        email_verified=email_verified,
    )
    db.session.add(user)
    db.session.commit()

    profile: Profile = Profile(
        user_uid=user_uid, img_type=None, email=None, school=None, bio=None
    )
    db.session.add(profile)
    db.session.commit()


class HS256JWTCodec:
    def __init__(self, key: str) -> None:
        self._key: Final[str] = key
        self._algorithm: Final[str] = "HS256"

    @property
    def key(self) -> str:
        return self._key

    @property
    def algorithm(self) -> str:
        return self._algorithm

    def encode(
        self,
        payload: dict[str, Any],
        expiration_time_delta: timedelta = timedelta(days=1),
    ) -> str:
        """Returns the JWT with `data`, Issue At (iat) and Expiration Time (exp) as payload."""
        current_time: datetime = datetime.now(tz=timezone.utc)
        expiration_time: datetime = current_time + expiration_time_delta
        payload = {
            "data": payload,
            "iat": current_time,
            "exp": expiration_time,
        }
        token: str = jwt.encode(payload, key=self._key, algorithm=self._algorithm)
        return token

    def decode(self, token: str) -> dict[str, Any]:
        data: dict[str, Any] = jwt.decode(
            token, key=self._key, algorithms=[self._algorithm]
        )
        return data

    def is_valid_jwt(self, token: str) -> bool:
        """Returns False if the expiration time (exp) is in the past or it failed validation."""
        try:
            self.decode(token)
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            return False
        return True


class FlaskThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app: Flask = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()
