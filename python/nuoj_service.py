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
import add_problem
import githubLogin
import googleLogin
import asanaUtil
import auth
import pytz

template_dir = "/opt/nuoj/templates"
app = Flask(__name__, static_url_path='', template_folder=template_dir)
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

@app.route("/edit_problem/<PID>/", methods=["GET", "POST"])
@app.route("/edit_problem/<PID>/basicSetting", methods=["GET", "POST"])
def returnEditProblemPage(PID):
	
	SID = request.cookies.get("SID")

	if(SID not in session):
		return redirect("/")

	data = session[SID]
	username = data["username"]

	if(username not in add_problem_map):
		return redirect("/")

	if(add_problem_map[username] != PID):
		return redirect("/")

	if(request.method == "GET"):
		return render_template("add_problem_bs.html", **locals())

	result = add_problem.post(conn, request.json, PID, username)

	return result

@app.route("/add_problem", methods=["GET", "POST"])
def returnAddProblemPage():

	SID = request.cookies.get("SID")

	if(SID not in session):
		return redirect("/")

	data = session[SID]
	username = data["username"]

	global add_problem_map
	
	add_problem_map[username] = os.urandom(10).hex()

	return redirect("/edit_problem/" + add_problem_map[username] + "/basicSetting")

@app.route("/submit", methods=["GET"], strict_slashes=False)
def returnSubmitPage():
	index_html = open("/opt/nuoj/html/submit.html", "r")
	return index_html.read()

@app.route("/problem", methods=["GET"])
def returnProblemPage():

	problem = []
	login = False
	username = None

	SID = request.cookies.get("SID")
	if(SID in session):
		login = True
		username = session[SID]["username"]

	for i in range(90):
		problem_dict = {"problem_ID": i+1, "problem_name": "A. 夏日祭", "problem_author": "ntut-xuan", "problem_tag": ["實作", "數學", "很難的題目", "week8", "星爆氣流斬 orz"]}
		problem.append(problem_dict)

	return render_template("problem.html", **locals())

@app.route("/submissions", methods=["GET"])
def returnSubmissionPage():
	index_html = open("/opt/nuoj/html/submissions.html", "r")
	return index_html.read()

@app.route("/login", methods=["GET", "POST"])
def returnLoginPage():
	settingJsonObject = json.loads(open("/opt/nuoj/setting.json", "r").read())
	githubStatus = settingJsonObject["oauth"]["github"]["enable"]
	googleStatus = settingJsonObject["oauth"]["google"]["enable"]
	if request.method == "GET":
		return render_template("login.html", **locals())
	data = request.json
	result = auth.login(conn, data)
	resp = Response(json.dumps(result), mimetype="application/json")

	if(result["status"] == "OK"):
		sessionID = os.urandom(16).hex()
		resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
		session[sessionID] = {"username": result["username"], "email": result["email"]}

	return resp

@app.route("/register", methods=["GET", "POST"])
def returnRegisterPage():
	settingJsonObject = json.loads(open("/opt/nuoj/setting.json", "r").read())
	githubStatus = settingJsonObject["oauth"]["github"]["enable"]
	googleStatus = settingJsonObject["oauth"]["google"]["enable"]
	verifyStatus = settingJsonObject["mail"]["enable"]
	if request.method == "GET":
		return render_template("register.html", **locals())

	data = request.json

	if data['check']:
		result = auth.VerifyCode(conn, data)
		resp = Response(json.dumps(result), mimetype="application/json")
		
		return resp
	else:
		result = auth.register(conn, data)
		resp = Response(json.dumps(result), mimetype="application/json")

		if(result["status"] == "OK"):
			sessionID = os.urandom(16).hex()
			resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
			session[sessionID] = {"username": result["username"], "email": result["email"]}

		return resp

@app.route("/announcement", methods=["GET"])
def getAnnouncement():
	announcementFile = open("/opt/nuoj/markdown/announcement.md", "r")
	return announcementFile.read()

@app.route("/submissionList", methods=["GET"])
def submissionList():
	conn = connect_mysql()
	result = None
	try:
		with conn.cursor() as cursor:
			command = "select * from submission"
			cursor.execute(command)
			result = cursor.fetchall()
			cursor.close()
			conn.close()
	except Exception as ex:
		logger.error(ex)
	data = {}
	submissionData = []
	for i in range (0, len(result)):
		subDict = {}
		subDict["submissionID"] = result[i][0]
		subDict["submissionTime"] = result[i][1]
		subDict["submissionBy"] = result[i][2]
		subDict["Language"] = result[i][3]
		subDict["ProblemID"] = result[i][4]
		subDict["VerdictResult"] = result[i][5]
		subDict["VerdictTime"] = result[i][6]
		subDict["VerdictMemory"] = result[i][7]
		submissionData.append(subDict)
	data["DataCount"] = len(result)
	data["SubmissionData"] = submissionData
	return json.dumps(data)

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

@app.route("/problemList", methods=["GET"])
def returnProblemList():
	
	with conn.cursor() as cursor:
		cursor.execute("SELECT ID,name,author from `problem`")
		datas = cursor.fetchall()
		cursor.close()
	
	result = {"status": "OK", "result": []}

	for data in datas:
		problem_data = {}
		problem_data["ID"] = data[0]
		problem_data["name"] = data[1]
		problem_data["author"] = data[2]
		result["result"].append(problem_data)
	
	return Response(json.dumps(result), mimetype="application/json")

@app.route("/problem/<PID>", methods=["GET", "POST"])
def returnProblemIDPage(PID):
	with conn.cursor() as cursor:
		cursor.execute("SELECT token FROM `problem` where ID=%s", PID)
		token = cursor.fetchone()[0]
	problemJsonObject = json.loads(open("/opt/nuoj/problem/" + token + "/problem.json", "r").read())
	title = problemJsonObject["problemContent"]["title"]
	description = problemJsonObject["problemContent"]["description"].replace("\n", "<br>")
	input_description = problemJsonObject["problemContent"]["input"].replace("\n", "<br>")
	output_description = problemJsonObject["problemContent"]["output"].replace("\n", "<br>")
	note = problemJsonObject["problemContent"]["note"].replace("\n", "<br>")
	TL = problemJsonObject["basicSetting"]["timeLimit"]
	ML = problemJsonObject["basicSetting"]["memoryLimit"]
	return render_template("problem_page.html", **locals())

@app.route("/profile/<name>", methods=["GET"])
def returnProfilePageWithName(name):
	try:    
		with conn.cursor() as cursor:
			cursor.execute("SELECT * from `user` where username=%s", (name))
			data  = cursor.fetchone()
			username = data[1]
			admin = data[4]
			cursor.close()
	except Exception as ex:
		print(ex)
	school = "未知"
	accountType = "使用者"
	if (admin == 1):
		accountType = "管理員"
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