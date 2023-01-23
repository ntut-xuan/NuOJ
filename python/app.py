#!/usr/bin/env python3
import json
from typing import Mapping, Any
from flask import Flask, send_from_directory
from flask.wrappers import Response

from app_add_problem import problem
from app_auth import auth
from app_problem import problem_page
from app_profile import profile_page
from page.route import page
import crypto_util

def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
	app = Flask(__name__, static_url_path='', template_folder="/etc/nuoj/templates")
 
	if test_config is None:
		app.config.from_pyfile("config.py")
	else:
		app.config.from_mapping(test_config)
 
	app.register_blueprint(auth)
	app.register_blueprint(problem)
	app.register_blueprint(problem_page)
	app.register_blueprint(profile_page)
	app.register_blueprint(page)

	@app.route("/static/<path:path>")
	def fetch_static_file_from_specific_path(path):
		return send_from_directory('../static', path)

	@app.route("/heartbeat", methods=["GET"])
	def fetch_heartbeat():
		return Response(json.dumps({"status": "OK"}), mimetype="application/json")

	crypto_util.GenerateKey()
	return app