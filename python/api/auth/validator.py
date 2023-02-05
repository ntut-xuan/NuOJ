import re
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, TypeVar

from flask import Response, request

from api.auth.auth_util import LoginPayload, RegisterPayload
from models import User
from util import make_simple_error_response

T = TypeVar("T")

def validate_login_payload_format_or_return_bad_request(func: Callable[..., Response | T]) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        assert payload is not None
        
        try:
            LoginPayload(**payload)
        except TypeError:
            return make_simple_error_response(HTTPStatus.BAD_REQUEST, "Wrong payload format")
        
        return func(*args, **kwargs)
    return wrapper

def validate_register_payload_format_or_return_bad_request(func: Callable[..., Response | T]) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        
        assert payload is not None
        
        try:
            RegisterPayload(**payload)
        except TypeError:
            return make_simple_error_response(HTTPStatus.BAD_REQUEST, "Wrong payload format.")
        
        return func(*args, **kwargs)
    return wrapper

def validate_email_or_return_unprocessable_entity(func: Callable[..., Response | T]) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        
        assert payload is not None
        assert "email" in payload
        
        email = payload["email"]
        is_email_valid = bool(re.match(r"^[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*@[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*(\.[A-Za-z0-9_]{2,3})+$", email))
        
        if not is_email_valid:
            return make_simple_error_response(HTTPStatus.UNPROCESSABLE_ENTITY, "Email is invalid.")
        
        return func(*args, **kwargs)
    return wrapper

def validate_handle_or_return_unprocessable_entity(func: Callable[..., Response | T]) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        
        assert payload is not None
        assert "handle" in payload
        
        handle = payload["handle"]
        is_handle_valid = bool(re.match("[a-zA-Z\d](?:[a-zA-Z\d]|[_-](?=[a-zA-Z\d])){3,38}$", handle))
        
        if not is_handle_valid:
            return make_simple_error_response(HTTPStatus.UNPROCESSABLE_ENTITY, "Handle is invalid.")
        
        return func(*args, **kwargs)
    return wrapper

def validate_password_or_return_unprocessable_entity(func: Callable[..., Response | T]) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        
        assert payload is not None
        assert "password" in payload
        
        password = payload["password"]
        is_password_valid = bool(re.match("(?=.*?[a-zA-Z])(?=.*?[0-9]).{8,}$", password))
        
        if not is_password_valid:
            return make_simple_error_response(HTTPStatus.UNPROCESSABLE_ENTITY, "Password is invalid.")
        
        return func(*args, **kwargs)
    return wrapper

def validate_handle_is_not_repeated_or_return_forbidden(func: Callable[..., Response | T]) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        
        assert payload is not None
        assert "handle" in payload
        
        handle = payload["handle"]
        user: User | None = User.query.filter_by(handle=handle).first()
        
        if user is not None:
            return make_simple_error_response(HTTPStatus.FORBIDDEN, "Handle is repeated.")
        
        return func(*args, **kwargs)
    return wrapper

def validate_email_is_not_repeated_or_return_forbidden(func: Callable[..., Response | T]) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        
        assert payload is not None
        assert "email" in payload
        
        email = payload["email"]
        user: User | None = User.query.filter_by(email=email).first()
        
        if user is not None:
            return make_simple_error_response(HTTPStatus.FORBIDDEN, "Email is repeated.")
        
        return func(*args, **kwargs)
    return wrapper
