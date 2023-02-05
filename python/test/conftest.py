import tempfile
import os
import shutil
from pathlib import Path
from typing import Generator

import pytest

from app import create_app
from database import create_db
from flask import Flask
from flask.testing import FlaskClient

@pytest.fixture
def app() -> Generator[Flask, None, None]:
    db_fp, db_path = tempfile.mkstemp()
    storage_path = tempfile.mkdtemp()
    app: Flask = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "STORAGE_PATH": storage_path
        }
    )
    _create_storage_folder_structure(storage_path)
    with app.app_context():
        create_db()
    
    yield app
    
    os.close(db_fp)
    os.unlink(db_path)
    shutil.rmtree(storage_path)

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def _create_storage_folder_structure(storage_path):
    (Path(storage_path) / "problem/").mkdir()
    (Path(storage_path) / "user_avater/").mkdir()
    (Path(storage_path) / "user_profile/").mkdir()
    (Path(storage_path) / "user_submission/").mkdir()
