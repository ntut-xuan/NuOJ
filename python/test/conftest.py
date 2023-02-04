import tempfile
import os
from typing import Generator

import pytest

from app import create_app
from database import create_db
from flask import Flask
from flask.testing import FlaskClient

@pytest.fixture
def app() -> Generator[Flask, None, None]:
    db_fp, db_path = tempfile.mkstemp()
    app: Flask = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            
        }
    )
    with app.app_context():
        create_db()
    
    yield app
    
    os.close(db_fp)
    os.unlink(db_path)

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
