from pathlib import Path

import pytest
from flask import Flask

from storage.util import (
    TunnelCode,
    delete_file,
    is_file_exists,
    read_file,
    read_file_bytes,
    write_file,
    write_file_bytes,
)


def get_test_file_path(app: Flask):
    storage_path: str = Path(app.config["STORAGE_PATH"])
    file_path: Path = storage_path / "user_profile" / "test_file"
    return file_path


@pytest.fixture
def create_test_file(app: Flask):
    with app.app_context():
        file_path: Path = get_test_file_path(app)
        file_path.touch()


class TestIsFileExists:
    def test_with_exist_file_should_return_true(
        self, app: Flask, create_test_file: None
    ):
        with app.app_context():

            assert is_file_exists("test_file", TunnelCode.USER_PROFILE)

    def test_with_not_exist_file_should_return_false(self, app: Flask):
        with app.app_context():

            assert not is_file_exists("test_file", TunnelCode.USER_PROFILE)


class TestWriteFile:
    def test_write_exists_file_should_write_string_to_file(
        self, app: Flask, create_test_file: None
    ):
        with app.app_context():
            file_path: Path = get_test_file_path(app)

            write_file("test_file", "some_test_string", TunnelCode.USER_PROFILE)

            text: str = Path.read_text(file_path)
            assert text == "some_test_string"

    def test_write_not_exists_file_should_create_file_and_write_string_to_file(
        self, app: Flask
    ):
        with app.app_context():
            file_path: Path = get_test_file_path(app)
            assert not file_path.exists()

            write_file("test_file", "some_test_string", TunnelCode.USER_PROFILE)

            assert file_path.exists()
            text: str = Path.read_text(file_path)
            assert text == "some_test_string"

    def test_write_bytes_to_exists_file_should_write_string_to_file(
        self, app: Flask, create_test_file: None
    ):
        with app.app_context():
            file_path: Path = get_test_file_path(app)

            write_file_bytes("test_file", b"some_test_string", TunnelCode.USER_PROFILE)

            file_bytes: bytes = Path.read_bytes(file_path)
            assert file_bytes == b"some_test_string"

    def test_write_bytes_to_not_exists_file_should_create_file_and_write_string_to_file(
        self, app: Flask
    ):
        with app.app_context():
            file_path: Path = get_test_file_path(app)
            assert not file_path.exists()

            write_file_bytes("test_file", b"some_test_string", TunnelCode.USER_PROFILE)

            assert file_path.exists()
            file_bytes: bytes = Path.read_bytes(file_path)
            assert file_bytes == b"some_test_string"


class TestReadFile:
    def test_read_string_from_exists_file_should_read_string_from_file(
        self, app: Flask, create_test_file: None
    ):
        with app.app_context():
            file_path: Path = get_test_file_path(app)
            file_path.write_text("some_test_string")

            text: str = read_file("test_file", TunnelCode.USER_PROFILE)

            assert text == "some_test_string"

    def test_read_string_from_absent_file_should_return_empty_string(self, app: Flask):
        with app.app_context():

            text: str = read_file("test_file", TunnelCode.USER_PROFILE)

            assert text == ""

    def test_read_bytes_from_exists_file_should_read_bytes_from_file(
        self, app: Flask, create_test_file: None
    ):
        with app.app_context():
            file_path: Path = get_test_file_path(app)
            file_path.write_bytes(b"some_test_string")

            text: str = read_file_bytes("test_file", TunnelCode.USER_PROFILE)

            assert text == b"some_test_string"

    def test_read_bytes_from_bsent_file_should_return_empty_bytes(self, app: Flask):
        with app.app_context():

            text: str = read_file_bytes("test_file", TunnelCode.USER_PROFILE)

            assert text == b""


class TestDeleteFile:
    def test_delete_exists_file_should_delete_the_test_file(
        self, app: Flask, create_test_file: None
    ):
        with app.app_context():
            test_file: Path = get_test_file_path(app)
            assert test_file.exists()

            delete_file("test_file", TunnelCode.USER_PROFILE)

            assert not test_file.exists()

    def test_delete_absent_file_should_do_nothing(self, app: Flask):
        with app.app_context():
            test_file: Path = get_test_file_path(app)
            assert not test_file.exists()

            delete_file("test_file", TunnelCode.USER_PROFILE)

            assert not test_file.exists()
