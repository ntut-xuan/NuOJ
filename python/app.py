import json
from secrets import token_hex
from pathlib import Path
from typing import Mapping, Any

from flask import Flask, send_from_directory, render_template
from flask.wrappers import Response

from api.auth.api_route import auth_bp
from api.problem.route import problem_bp
from api.profile.route import profile_bp
from api.auth.test_route import auth_test_bp
from database import create_db_command, db
from page.auth.route import auth_page_bp
from page.problem.route import problem_page_bp
from page.profile.route import profile_page_bp
from page.submission.route import submission_page_bp
from page.route import page
from setting.util import Setting, SettingBuilder


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, static_url_path="", template_folder="/etc/nuoj/templates")

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.from_mapping(test_config)

    app.config["jwt_key"] = token_hex()
    app.config["mail_verification_code"] = {}
    app.config["setting"] = SettingBuilder().from_json_file(
        Path("/etc/nuoj/setting.json")
    )

    db.init_app(app)

    app.cli.add_command(create_db_command)
    app.register_blueprint(auth_bp)
    app.register_blueprint(problem_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(profile_page_bp)
    app.register_blueprint(auth_test_bp)
    app.register_blueprint(auth_page_bp)
    app.register_blueprint(page)
    app.register_blueprint(problem_page_bp)
    app.register_blueprint(submission_page_bp)

    @app.route("/static/<path:path>")
    def fetch_static_file_from_specific_path(path):
        return send_from_directory("../static", path)

    @app.route("/heartbeat", methods=["GET"])
    def fetch_heartbeat():
        return Response(json.dumps({"status": "OK"}), mimetype="application/json")

    # crypto_util.GenerateKey()
    return app
