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
from datetime import timedelta
import time;
import add_problem
import githubLogin
import googleLogin

app = Flask(__name__, static_url_path='/opt/nuoj/static')
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.secret_key = os.urandom(16).hex()

CORS(app)
isolate_path = ""

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

@app.route("/edit_problem", methods=["GET"])
def returnEditProblemPage():
	pass

@app.route("/add_problem", methods=["GET", "POST"])
def returnAddProblemPage():

	SID = request.cookies.get("SID")

	if(SID not in session):
		return redirect("/")

	html = open("/opt/nuoj/html/add_problem.html", "r")

	if request.method == "POST":
		username = session[SID]["username"]
		return add_problem.post(conn, request.json, username)

	return html.read()

@app.route("/submit", methods=["GET"], strict_slashes=False)
def returnSubmitPage():
	index_html = open("/opt/nuoj/html/submit.html", "r")
	return index_html.read()

@app.route("/problem", methods=["GET"])
def returnProblemPage():
	index_html = open("/opt/nuoj/html/problem.html", "r")
	return index_html.read()

@app.route("/submissions", methods=["GET"])
def returnSubmissionPage():
	index_html = open("/opt/nuoj/html/submissions.html", "r")
	return index_html.read()

@app.route("/login", methods=["GET"])
def returnLoginPage():
	index_html = open("/opt/nuoj/html/login.html", "r")
	if request.method == "GET":
		return index_html.read()

@app.route("/queryProblemID", methods=["GET"])
def getAvailableProblemID():
	try:
		with conn.cursor() as cursor:
			cursor.execute("SELECT COUNT(*) from `problem`")
			count = cursor.fetchone()[0]
	except Exception as ex:
			print(ex)
	data = {}
	data["Status"] = "OK"
	data["Result"] = {"Count": count}
	return json.dumps(data)

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

@app.route("/problem/<PID>", methods=["GET", "POST"])
def returnProblemIDPage(PunauthorizedID):
	page = open("/opt/nuoj/html/problem_page.html", "r")
	if request.method == "GET":
		return page.read()
	data = open("/opt/nuoj/problem/" + PID + "/problem.json")
	return data.read()

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
	
	data = githubLogin.githubLogin(conn, request.args.get("code"))

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

	data = googleLogin.googleLogin(conn, request.args)

	if(data["status"] == "OK"):
		resp = redirect("/")
		sessionID = os.urandom(16).hex()
		resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
		session[sessionID] = {"username": data["user"], "email": data["email"]}
		return resp
	else:
		return Response(json.dumps(data), mimetype="application/json")

if __name__ == "__main__":
	
	# Initilize isolate
	init_isolate()
	# Initilize mariadb
	conn = connect_mysql()
	
	settingJsonObject = json.loads(open("../setting.json", "r").read())

	app.debug = True

	if(settingJsonObject["cert"]["enable"] == False):
		app.run(host="0.0.0.0", port=80)
	else:
		app.run(host="0.0.0.0", port=443, ssl_context=(settingJsonObject["cert"]["fullchain_path"], settingJsonObject["cert"]["private_key_path"]))
