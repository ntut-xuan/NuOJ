#!/usr/bin/env python3
from uuid import uuid4
from flask import *
from flask.wrappers import Response
import os
import json
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
from dateutil import parser
import time;
import github_login_util as github_login_util
import google_login_util as google_login_util
import asana_util as asana_util
import jwt
import pytz
import auth_util
import hashlib
from error_code import error_dict, ErrorCode 
import database_util as database_util
import crypto_util as crypto_util
from tunnel_code import TunnelCode
import setting_util as setting_util
from app_auth import auth
from app_add_problem import problem
from app_problem import problem_page
from app_profile import profile_page
from app_admin import admin_page


app = Flask(__name__, static_url_path='', template_folder="/etc/nuoj/templates")
app.register_blueprint(auth)
app.register_blueprint(problem)
app.register_blueprint(problem_page)
app.register_blueprint(profile_page)

asana_util = asana_util.AsanatUil(json.loads(open("/etc/nuoj/setting.json", "r").read())["asana"]["token"])
# app.json.sort_keys = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.secret_key = os.urandom(16).hex()

CORS(app)
isolate_path = ""
add_problem_map = {}

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internel_server_error(error):
    return render_template('500.html', error=error)

@app.errorhandler(418)
def im_a_teapot(error):
	return render_template('418.html', error=error)

@app.route("/veriCookie")
def veriCookie(cookie):
	data = {}
	if cookie in session:
		data["status"] = "OK"
		data["result"] = {"cookie": session[cookie]}
	else:
		data["status"] = "Failed"
	return json.dumps(data)

@app.route("/pubkey")
def pubkey():
	return send_from_directory('../', "public.pem")

@app.route("/static/<path:path>")
def returnStaticFile(path):
	return send_from_directory('../static', path)

@app.route("/", methods=["GET"])
def returnIndex():
	SID = request.cookies.get("SID")
	login = (SID in session)

	if login:
		handle = session[SID]["handle"]

	return render_template("index.html", **locals())

@app.route("/problem", methods=["GET"])
def returnProblemPage():

	problem = []
	problem_db = database_util.command_execute("SELECT * from `problem`", ())

	SID = request.cookies.get("SID")
	login = (SID in session)
	
	if login:
		username = session[SID]["handle"]

	for i in range(len(problem_db)):
		raw_problem_data = database_util.file_storage_tunnel_read(problem_db[i]["problem_pid"] + ".json", TunnelCode.PROBLEM)
		problem_id = problem_db[i]["ID"]
		problem_author = problem_db[i]["problem_author"]
		if len(raw_problem_data) == 0:
			continue
		problem_data = json.loads(raw_problem_data)
		if "problem_content" in problem_data:
			problem_content = problem_data["problem_content"]
			problem_title = problem_content["title"]
			problem_dict = {"problem_ID": problem_id, "problem_name": problem_title, "problem_author": problem_author, "problem_tag": []}
			problem.append(problem_dict)

	return render_template("problem.html", **locals())

@app.route("/logout", methods=["GET", "POST"])
def logout():
	resp = Response(json.dumps({"status": "OK"}))
	resp.set_cookie("SID", value = "", expires=0)
	return resp


@app.route("/dev_progress", methods=["GET"])
def progressPage():

	fetch_section_id = ["1202538198680473", "1202538198680519", "1202538198680522", "1202538198680525", "1202561659397276", "1202561659397287"]
	section_color = ["bg-orange-400", "bg-green-400", "bg-blue-400", "bg-purple-400", "bg-cyan-400", "bg-teal-400"]
	completed_task = asana_util.get_tasks("1202538198680466")
	task_count_by_section = {}
	complete_task_count_by_section = {}
	section_complete_percentage = {}
	section_task_info = {}
	completed_task_info = []

	for task in completed_task:
		task_section_gid = task["memberships"][0]["section"]["gid"]
		task_section_name = task["memberships"][0]["section"]["name"]
		if task_section_gid not in task_count_by_section:
			task_count_by_section[task_section_gid] = 0
			complete_task_count_by_section[task_section_gid] = 0
			section_task_info[task_section_gid] = []
		task_count_by_section[task_section_gid] += 1
		if task["completed"] and task_section_gid in fetch_section_id:
			index = fetch_section_id.index(task_section_gid)
			card_background_color = section_color[index]
			completed_time = parser.parse(task["completed_at"]).astimezone(pytz.timezone("Asia/Taipei"))
			completed_time_string = datetime.strftime(completed_time, "%Y-%m-%d %H:%M:%S")
			assignee_photo = None
			if task["assignee"]["photo"] == None:
				assignee_photo = "/static/logo_min.png"
			else:
				assignee_photo = task["assignee"]["photo"]["image_128x128"]
			completed_task_info.append({
				"task_section_name": task_section_name, "task_name": task["name"], 
				"task_complete_time": completed_time_string, "task_assignee": task["assignee"]["name"], 
				"task_assignee_photo": assignee_photo, "task_color": card_background_color})
			complete_task_count_by_section[task_section_gid] += 1
		section_complete_percentage[task_section_gid] = complete_task_count_by_section[task_section_gid] / task_count_by_section[task_section_gid]

	completed_task_info = sorted(completed_task_info, key=lambda d : d["task_complete_time"], reverse=True)
	frontend_pc = int(section_complete_percentage["1202538198680473"] * 100)
	backend_pc = int(section_complete_percentage["1202538198680519"] * 100)
	judge_pc = int(section_complete_percentage["1202538198680522"] * 100)
	other_pc = int(section_complete_percentage["1202538198680525"] * 100)
	database_pc = int(section_complete_percentage["1202561659397276"] * 100)
	test_pc = int(section_complete_percentage["1202561659397287"] * 100)
	complete_pc = (frontend_pc + backend_pc + judge_pc + other_pc + database_pc) // 5
	
	return render_template("progress.html", **locals())

@app.route("/about", methods=["GET"])
def getAboutIndex():
	return render_template("about_us.html", **locals())

@app.route("/debug", methods=["GET"])
def getDebugPage():
	return render_template("debug.html", **locals())

@app.route("/status", methods=["GET"])
def getStatusPage():
	def status_to_plain_text(status: int) -> str:
		return "工作中" if status == 200 else "連接失敗"
	def status_to_color(status: int) -> str:
		return "bg-green-500" if status == 200 else "bg-red-500"
	def data_proc(data: dict) -> dict:
		return {
			"name": data["name"], 
			"status": status_to_plain_text(data["status"]), 
			"status_color": status_to_color(data["status"])
		} 
	web_app_heartbeat_info = [data_proc(data) for data in setting_util.web_app_heartbeat_check()]
	database_heartbeat_info = [data_proc(data) for data in setting_util.database_heartbeat_check()]
	judge_server_heartbeat_info = [data_proc(data) for data in setting_util.judge_server_heartbeat_check()]
	return render_template("status.html", **locals())

@app.route("/heartbeat", methods=["GET"])
def getHeartbeat():
	return Response(json.dumps({"status": "OK"}), mimetype="application/json")

if __name__ == "__main__":

	settingJsonObject = json.loads(open("/etc/nuoj/setting.json", "r").read())

	conn = database_util.connect_database()
	result = database_util.command_execute("SELECT * FROM `user`", ())
	crypto_util.GenerateKey()
	
	app.debug = True

	if app.debug == True:
		payload = {"handle": "nuoj_test", "email": "nuoj_test@nuoj.net", "iat": datetime.now(tz=timezone.utc), "exp": datetime.now(tz=timezone.utc) + timedelta(days=365)}
		print(jwt.encode(payload, "secret", algorithm="HS256"))

		test_account_exist = database_util.command_execute('SELECT COUNT(*) FROM `user` WHERE handle="nuoj_test"', ())[0]["COUNT(*)"]
		password = auth_util.password_cypto("nuoj223344")
		if test_account_exist == 0:
			database_util.command_execute('INSERT INTO `user`(user_uid, handle, password, email, role, email_verified) VALUES("40ff8688-4142-459f-8f3a-aaecb6312d87", "nuoj_test", %s, "nuoj_test@nuoj.net", 0, 1) ', (password))

	if(settingJsonObject["cert"]["enable"] == False):
		app.run(host="0.0.0.0", port=80, threaded=True)
	else:
		app.run(host="0.0.0.0", port=443, ssl_context=(settingJsonObject["cert"]["fullchain_path"], settingJsonObject["cert"]["private_key_path"]), threaded=True)