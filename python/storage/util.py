import os
from enum import Enum

from flask import current_app


class TunnelCode(Enum):
    PROBLEM = "problem"
    TESTCASE = "testcase"
    SOLUTION = "problem_solution"
    CHECKER = "problem_checker"
    USER_AVATER = "user_avater"
    SUBMISSION = "user_submission"
    USER_PROFILE = "user_profile"


def is_file_exists(filename: str, tunnel: TunnelCode) -> bool:
    file_path = _make_file_path(tunnel, filename)
    return os.path.exists(file_path)


def read_file(filename: str, tunnel: TunnelCode) -> str:
    file_path = _make_file_path(tunnel, filename)
    if is_file_exists(filename, tunnel):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return ""


def read_file_bytes(filename: str, tunnel: TunnelCode) -> bytes:
    file_path = _make_file_path(tunnel, filename)
    if is_file_exists(filename, tunnel):
        with open(file_path, "rb") as file:
            return file.read()
    else:
        return b""


def write_file(filename: str, data: str, tunnel: TunnelCode) -> None:
    file_path = _make_file_path(tunnel, filename)
    with open(file_path, "w") as file:
        file.write(data)
        file.close()


def write_file_bytes(filename: str, data: bytes, tunnel: TunnelCode) -> None:
    file_path = _make_file_path(tunnel, filename)
    with open(file_path, "wb") as file:
        file.write(data)
        file.close()


def delete_file(filename: str, tunnel: TunnelCode) -> None:
    file_path = _make_file_path(tunnel, filename)
    if is_file_exists(filename, tunnel):
        os.remove(file_path)


def _make_file_path(tunnel: TunnelCode, filename: str) -> str:
    storage_path = current_app.config.get("STORAGE_PATH")
    assert storage_path is not None
    file_path = "%s/%s/%s" % (storage_path, tunnel.value, filename)
    return file_path
