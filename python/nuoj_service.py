#!/usr/bin/env python3
from flask import *
import subprocess
from flask.wrappers import Response
import pymysql
import os
import json
from flask_cors import cross_origin, CORS
from datetime import datetime as dt
from uuid import uuid4
from loguru import logger
from flask_session import Session
from datetime import datetime, timedelta
from dateutil import parser
import time;
import githubLogin
import googleLogin
import asanaUtil
import pytz
import requests
import database
from app_auth import auth
from app_add_problem import problem

app = Flask(__name__, static_url_path='', template_folder="/opt/nuoj/templates")
app.register_blueprint(auth)
app.register_blueprint(problem)

asana_util = asanaUtil.AsanatUil(json.loads(open("/opt/nuoj/setting.json", "r").read())["asana"]["token"])
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.secret_key = os.urandom(16).hex()

CORS(app)
isolate_path = ""

add_problem_map = {}

def init_isolate():
	
	# clean up isolate
	result = subprocess.run("isolate --cleanup".split(), stdout=subprocess.PIPE)
	logger.debug(result.stdout.decode("utf-8").replace('\n',''))
	logger.info("ISOLATE_INIT (1/2) CLEANUP")

	# init isolate
	result = subprocess.run("isolate --init".split(), stdout=subprocess.PIPE)
	isolate_path = result.stdout.decode("utf-8").replace('\n','')
	logger.debug(isolate_path)
	logger.info("ISOLATE_INIT (2/2) INIT")

def init_verifycode():
	
	# init verifycode
	code = {}
	file = open("/tmp/verify_code", "w")
	json.dump(code, file)
	file.close()
	

def connect_mysql():
	
	# connect NuOJ Database
	db_setting = {
		"host": "localhost",
		"port": 3306,
		"user": "NuOJService",
		"password": "Nu0JS!@#$",
		"db": "NuOJ",
		"charset": "utf8"
	}
	conn = None
	try:
		conn = pymysql.connect(**db_setting)
		logger.info("MYSQL_INIT (1/1) INIT")
	except Exception as ex:
		print(ex)
	finally:
		return conn

def connect_database():
	setting = json.loads(open("/opt/nuoj/setting.json", "r").read())
	database_list = setting["database"]
	for data in database_list:
		url = data["url"] + ":" + data["port"] 
		print(url)
		req = requests.get(url + "/heartbeat")
		if req.status_code == 200:
			return url
	return None

def nuoj_getID(conn):
	reuslt = ""
	try:
		with conn.cursor() as cursor:
			command = "select COUNT(*) from submission"
			cursor.execute(command)
			result = str(cursor.fetchone()[0])
			logger.info(result) # fetch result
			cursor.close()
			conn.close()
	except Exception as ex:
		logger.error(ex)
	finally:
		return int(result)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internel_server_error(error):
    return render_template('500.html', error=error)

@app.route("/veriCookie")
def veriCookie(cookie):
	data = {}
	if cookie in session:
		data["status"] = "OK"
		data["result"] = {"cookie": session[cookie]}
	else:
		data["status"] = "Failed"
	return json.dumps(data)

@app.route("/static/<path:path>")
def returnStaticFile(path):
	return send_from_directory('../static', path)

@app.route("/", methods=["GET", "POST"])
def returnIndex():
	index_html = open("/opt/nuoj/html/index.html", "r")
	if request.method == "GET":
		return index_html.read()
	
	SID = request.cookies.get("SID")
	return veriCookie(SID)

@app.route("/add_problem", methods=["GET", "POST"])
def returnAddProblemPage():

	SID = request.cookies.get("SID")

	if(SID not in session):
		return redirect("/")

	data = session[SID]
	username = data["username"]

	n = len(database.get_data("/problems/", {})["data"])

	data_dict = {"problem_pid": os.urandom(10).hex(), "problem_author": username, "index": n+1}

	database.post_data("/problems/", {}, json.dumps(data_dict))
	return redirect("/edit_problem/" + data_dict["problem_pid"] + "/basicSetting")

@app.route("/submit", methods=["GET"], strict_slashes=False)
def returnSubmitPage():
	index_html = open("/opt/nuoj/html/submit.html", "r")
	return index_html.read()

@app.route("/problem", methods=["GET"])
def returnProblemPage():

	problem = []

	problem_db = database.get_data("/problems/", {})["data"]

	for i in range(len(problem_db)):
		problem_content = problem_db[i]["problem_content"]
		problem_author = problem_db[i]["problem_author"]
		problem_dict = {"problem_ID": i+1, "problem_name": problem_content["title"], "problem_author": problem_author, "problem_tag": []}
		problem.append(problem_dict)

	return render_template("problem.html", **locals())

@app.route("/logout", methods=["GET", "POST"])
def logout():
	data = {}
	data["status"] = "OK"
	data["message"] = "Logout successful."
	code = 200
	try:
		SID = request.cookies.get("SID")
		if(SID in session):
			del session[SID]
	except Exception as ex:
		data["status"] = "Failed"
		data["message"] = ex
		code = 500
	resp = Response(response=json.dumps(data), status=code)
	return resp

@app.route("/problem/<ID>", methods=["GET", "POST"])
def returnProblemIDPage(ID):
	problemJsonObject = database.get_data("/problems/", {"index": ID})["data"][0]
	title = problemJsonObject["problem_content"]["title"]
	description = problemJsonObject["problem_content"]["description"].replace("\n", "<br>")
	input_description = problemJsonObject["problem_content"]["input"].replace("\n", "<br>")
	output_description = problemJsonObject["problem_content"]["output"].replace("\n", "<br>")
	note = problemJsonObject["problem_content"]["note"].replace("\n", "<br>")
	TL = problemJsonObject["basic_setting"]["time_limit"]
	ML = problemJsonObject["basic_setting"]["memory_limit"]
	return render_template("problem_page.html", **locals())

@app.route("/profile/<name>", methods=["GET"])
def returnProfilePageWithName(name):
	user_db = database.get_data("/users/" + name, {})
	admin = user_db["data"]["admin"]
	username = name
	school = "未知"
	accountType = "使用者" if admin == 0 else "管理員"
	return render_template("profile.html", **locals())

@app.route("/github_login", methods=["GET", "POST"])
def processGithubLogin():
	
	settingJsonObject = json.loads(open("/opt/nuoj/setting.json", "r").read())
	data = githubLogin.githubLogin(conn, request.args.get("code"), settingJsonObject)

	if(data["status"] == "OK"):
		resp = redirect("/")
		sessionID = os.urandom(16).hex()
		resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
		session[sessionID] = {"username": data["user"], "email": data["email"]}
		return resp
	else:
		return Response(json.dumps(data), mimetype="application/json")

@app.route("/google_login", methods=["GET", "POST"])
def processGoogleLogin():

	settingJsonObject = json.loads(open("/opt/nuoj/setting.json", "r").read())
	data = googleLogin.googleLogin(conn, request.args, settingJsonObject)
	
	if(data["status"] == "OK"):
		resp = redirect("/")
		sessionID = os.urandom(16).hex()
		resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
		session[sessionID] = {"username": data["user"], "email": data["email"]}
		return resp
	else:
		return Response(json.dumps(data), mimetype="application/json")

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

if __name__ == "__main__":
	
	# Initilize isolate
	init_isolate()
	# Initilize verifycode
	init_verifycode()
	# Initilize mariadb
	conn = connect_mysql()

	settingJsonObject = json.loads(open("/opt/nuoj/setting.json", "r").read())

	app.debug = True

	if(settingJsonObject["cert"]["enable"] == False):
		app.run(host="0.0.0.0", port=80, threaded=True)
	else:
		app.run(host="0.0.0.0", port=443, ssl_context=(settingJsonObject["cert"]["fullchain_path"], settingJsonObject["cert"]["private_key_path"]), threaded=True)