from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from click.testing import Result
    from flask import Flask
    from flask.testing import FlaskCliRunner


def test_create_db_command(app: Flask) -> None:
    with app.app_context():
        runner: FlaskCliRunner = app.test_cli_runner()

        result: Result = runner.invoke(args=("create-db",))

    assert result.exit_code == 0
    assert result.output == "Created the database.\n"
