import tempfile
import os
import shutil
from http import HTTPStatus
from pathlib import Path
from typing import Any, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from requests import Response, delete
from werkzeug.test import TestResponse

from app import create_app
from api.auth.email_util import MailSender, _get_mail_sender
from database import create_db, db
from models import User
from setting.util import Setting, SettingBuilder


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    db_fp, db_path = tempfile.mkstemp()
    storage_path = tempfile.mkdtemp()
    app: Flask = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "STORAGE_PATH": storage_path,
        }
    )
    _setup_setting_to_app_config(app)
    _create_storage_folder_structure(storage_path)
    with app.app_context():
        create_db()
        _add_test_account()
        _remove_all_email_from_fake_smtp_server()

    yield app

    os.close(db_fp)
    os.unlink(db_path)
    shutil.rmtree(storage_path)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def logged_in_client(app: Flask) -> FlaskClient:
    client: FlaskClient = app.test_client()
    response: TestResponse = client.post(
        "/api/auth/login", json={"account": "test_account", "password": "nuoj_test"}
    )
    assert response.status_code == HTTPStatus.OK
    return client


@pytest.fixture
def enabled_mail_setting(app: Flask) -> None:
    setting: Setting = app.config["setting"]
    setting.mail.enable = True


def _create_storage_folder_structure(storage_path):
    (Path(storage_path) / "problem/").mkdir()
    (Path(storage_path) / "problem_checker/").mkdir()
    (Path(storage_path) / "problem_solution/").mkdir()
    (Path(storage_path) / "testcase").mkdir()
    (Path(storage_path) / "user_avater/").mkdir()
    (Path(storage_path) / "user_profile/").mkdir()
    (Path(storage_path) / "user_submission/").mkdir()


def _add_test_account() -> None:
    user: User = User(
        user_uid="cb7ce8d5-8a5a-48e0-b9f0-7247dd5825dd",
        handle="test_account",
        password="cc28a9d01d08f4fa60b63434ce9971fda60e58a2f421898c78582bbb709bf7bb",  # nuoj_test
        email="test_account@nuoj.com",
        role=0,
        email_verified=0,
    )
    db.session.add(user)
    db.session.commit()


def _remove_all_email_from_fake_smtp_server() -> None:
    sender: MailSender = _get_mail_sender()
    server_url: str = "http://" + sender.server + ":1080/api/emails"

    response: Response = delete(server_url)

    assert response.status_code == HTTPStatus.OK


def _setup_setting_to_app_config(app: Flask) -> None:
    setting: dict[str, Any] = {
        "oauth": {
            "github": {
                "enable": True,
                "client_id": "some_client_id",
                "secret": "some_secret",
            },
            "google": {
                "enable": True,
                "client_id": "some_client_id",
                "secret": "some_secret",
                "redirect_url": "some_redirect_url",
            },
        },
        "mail": {
            "enable": False,
            "server": "fake-smtp-server",
            "port": "1025",
            "mailname": "test@nuoj.com",
            "password": "nuoj_test",
            "redirect_url": "http://test.net/mail_verification",
        },
        "asana": {"token": ""},
    }
    app.config["setting"] = SettingBuilder().from_dict(setting)
