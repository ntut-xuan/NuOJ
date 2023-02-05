#!/usr/bin/env python3
from flask import *
import os
import json
import hashlib
import re
import smtplib
import threading
import jwt
import database_util
import crypto_util as crypto_util
from datetime import *
from tunnel_code import TunnelCode
import setting_util as setting_util
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from error_code import ErrorCode, error_dict

from typing import Any, Final
from dataclasses import dataclass

from sqlalchemy.sql import or_, and_
from api.auth.email_util import send_verification_email
from database import db
from models import User, Profile


@dataclass
class LoginPayload:
    account: str
    password: str


@dataclass
class RegisterPayload:
    email: str
    handle: str
    password: str


def password_cypto(password) -> str:
    m = hashlib.sha256()
    m.update(password.encode("utf8"))
    password = m.hexdigest()
    return password

def login(account: str, password: str) -> bool:
    password = password_cypto(password)

    user: User | None = User.query.filter(and_(or_(User.email == account, User.handle == account), User.password == password)).first()

    if user == None:
        return False
    
    return True

def register(email: str, handle: str, password: str) -> None:
    # password = crypto_util.Decrypt(password)
    # response = {"status": "OK"}

    # Cypto
    password = password_cypto(password)
    
    # create user_uid
    user_uid = str(uuid4())
    
    # add user
    user: User = User(user_uid=user_uid, email=email, handle=handle, password=password, role=0, email_verified=0)
    db.session.add(user)
    db.session.commit()
    
    # init profile
    profile: Profile = Profile(user_uid=user_uid)
    db.session.add(profile)
    db.session.commit()
    
    # Write into storage (init)
    if not database_util.file_storage_tunnel_exist(user_uid + ".json", TunnelCode.USER_PROFILE):
        database_util.file_storage_tunnel_write(user_uid + ".json", json.dumps({"handle": handle, "email": email, "school": "", "bio": ""}), TunnelCode.USER_PROFILE)

    if setting_util.mail_verification_enable():
        thread = threading.Thread(target=send_verification_email, args=[handle, email])
        thread.start()


def handle_exist(email) -> bool:
    result = database_util.command_execute("SELECT handle FROM `user` WHERE email=%s", (email))[0]
    return result["handle"] != None

def handle_setup(data, email) -> dict:

    # User Data
    handle = data["handle"]

    # Validate handle
    handle_valid = bool(re.match("[a-zA-Z\\d](?:[a-zA-Z\\d]|[_-](?=[a-zA-Z\\d])){3,38}$", handle))
    if not handle_valid:
        return error_dict(ErrorCode.HANDLE_INVALID)
    
    # Check handle repeat or not
    result = database_util.command_execute("SELECT COUNT(*) FROM `user` WHERE handle=%s", (handle))[0]
    if result["COUNT(*)"] > 0:
        return error_dict(ErrorCode.HANDLE_REPEAT)

    # Setup Handle
    database_util.command_execute("UPDATE `user` SET handle=%s WHERE email=%s", (handle, email))

    # Setup Handle on storage data
    user_uid = database_util.command_execute("SELECT user_uid from `user` where email=%s", (email))[0]["user_uid"]
    database_util.file_storage_tunnel_write(user_uid + ".json", json.dumps({"handle": handle, "email": email, "school": "", "bio": ""}), TunnelCode.USER_PROFILE)      

    return {"status": "OK", "data": {"email": email, "handle": handle}}

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
