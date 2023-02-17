from __future__ import annotations

import sqlite3
from typing import Final

import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db: Final[SQLAlchemy] = SQLAlchemy()

# For SQLAlchemy.create_all to know what to create.
# NOTE: imports after the creation of "db" to resolve circular import
from models import User


# SQLite does not work with foreign key by default.
# The PRAGMA for enablement must be emitted on all connections before use.
# See https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor: sqlite3.Cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


@click.command("create-db")
def create_db_command() -> None:
    create_db()
    click.echo("Created the database.")


def create_db() -> None:
    with current_app.app_context():
        db.create_all()
