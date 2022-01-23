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
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_session import Session
from datetime import timedelta
import time;

app = Flask(__name__, static_url_path='/opt/nuoj/static')
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.secret_key = os.urandom(16).hex()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '登入NuOJ'

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

@app.route("/static/<path:path>")
def returnStaticFile(path):
    return send_from_directory('static', path)

@app.route("/", methods=["GET", "POST"])
def returnIndex():
    index_html = open("/opt/nuoj/html/index.html", "r")
    if request.method == "GET":
        return index_html.read()
    
    SID = request.cookies.get("SID")
    print(SID)
    data = {}
    if(SID in session):
        data["status"] = "OK"
        data["username"] = session[SID]["username"]
    else:
        data["status"] = "Failed"
    return json.dumps(data)
    

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

@app.route("/login", methods=["GET", "POST"])
def returnLoginPage():
    index_html = open("/opt/nuoj/html/login.html", "r")
    if request.method == "GET":
        return index_html.read()
    
    account = request.json['account']
    password = request.json['password']
    status = "OK"
    message = "登入成功"
    conn = connect_mysql()
    account_type = 1 # email = 0, username = 1

    if '@' in account:
        account_type = 0
    
    if account_type == 0:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM `user` WHERE email=%s", (account))
            result = cursor.fetchone()[0]
            if result == 0:
                status = "Failed"
                message = "登入失敗，信箱不存在"
            cursor.close()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM `user` WHERE email=%s AND password=%s", (account, password))
            result = cursor.fetchone()[0]
            if result == 0:
                status = "Failed"
                message = "登入失敗，信箱或密碼錯誤"
            cursor.close()
    else:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM `user` WHERE username=%s", (account))
            result = cursor.fetchone()[0]
            if result == 0:
                status = "Failed"
                message = "登入失敗，使用者帳號不存在"
            cursor.close()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM `user` WHERE username=%s AND password=%s", (account, password))
            result = cursor.fetchone()[0]
            if result == 0:
                status = "Failed"
                message = "登入失敗，使用者帳號或密碼錯誤"
            cursor.close()

    data = {}
    data["status"] = status
    data["message"] = message

    resp = Response(json.dumps(data))

    if(status == "OK"):

        sessionID = os.urandom(16).hex()
        username = ""
        email = ""
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT username FROM `user` WHERE username=%s OR email=%s", (account, account))
            username = cursor.fetchone()[0]
            cursor.execute("SELECT email FROM `user` WHERE username=%s OR email=%s", (account, account))
            email = cursor.fetchone()[0]
        
        resp.set_cookie("SID", value = sessionID, expires=time.time()+6*60)
        session[sessionID] = {"username": username, "email": email}

    return resp

@app.route("/register", methods=["GET", "POST"])
def returnRegisterPage():
    index_html = open("/opt/nuoj/html/register.html", "r")
    if request.method == 'GET':
        return index_html.read()
    
    username = request.json['user_id']
    email = request.json['email']
    password = request.json['password']
    conn = connect_mysql()
    status = "OK"
    message = "註冊成功"

    # check username registered.
    try:    
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) from `user` where username=%s", (username))
            count = cursor.fetchone()[0]
            if(count > 0):
                status = "Failed"
                message = "使用者名稱已被註冊"
            cursor.close()
    except Exception as ex:
        print(ex)
    
    # check email registered.
    try:    
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) from `user` where email=%s", (email))
            count = cursor.fetchone()[0]
            if(count > 0):
                status = "Failed"
                message = "信箱已被註冊"
            cursor.close()
    except Exception as ex:
        print(ex)

    if(status == "OK"):
        # really submit
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO `user` (username, email, password, admin) values (%s, %s, %s, 0)", (username, email, password))
                conn.commit()
                cursor.close()
        except Exception as ex:
            print(ex)
    
    data = {}
    data["status"] = status
    data["message"] = message

    sessionID = os.urandom(16).hex()

    resp = Response(json.dumps(data))
    resp.set_cookie("SID", value = sessionID, expires=time.time()+6*60)

    session[sessionID] = {"username": username, "email": email}

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

@app.route("/problemList", methods=["GET"])
def problemList():
    conn = connect_mysql()
    result = None
    try:
        with conn.cursor() as cursor:
            command = "select * from problem"
            cursor.execute(command)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
    except Exception as ex:
        logger.error(ex)
    data = {}
    problemData = []
    for i in range (0, len(result)):
        subDict = {}
        subDict["problem_id"] = result[i][0]
        subDict["problem_name"] = result[i][1]
        subDict["problem_deadline"] = result[i][2]
        subDict["problem_author"] = result[i][3]
        problemData.append(subDict)
    data["DataCount"] = len(result)
    data["problemData"] = problemData
    return json.dumps(data)

@app.route("/submit", methods=["POST"])
def submit():
    
    # Get user code from frontend
    code = str(request.json["code"])
    
    # Generate submissionID and submissionTIme
    conn = connect_mysql()
    submissionID = str(nuoj_getID(conn) + 1)
    submissionTime = str(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = "OK"
    
    # Some Info
    submissionBy = "Uriah"
    language = "C++"
    problemID = "a001"
    
    # Save code to tmp
    save_path = "/opt/nuoj/submit_code"
    file_name = "submission_" + str(submissionID) + ".cpp"
    completeName = os.path.join(save_path, file_name)
    file1 = open(completeName, "w")
    file1.write(code)
    file1.close()
    
    # Insert into mysql table
    conn = connect_mysql()
    try:
        with conn.cursor() as cursor:
            command = "INSERT INTO `submission` (submissionTime, submissionBy, ProblemID, Language, VerdictResult, VerdictTime, VerdictMemory) VALUES('%s', '%s', '%s', '%s', 'Pending', '', '');" % (submissionTime, submissionBy, problemID, language)
            cursor.execute(command)
            logger.info(command)
            result = str(cursor.fetchall())
            logger.info(result) # fetch result
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as ex:
        logger.error(ex)
        status = "Failed"
    
    data = {}

    data["Status"] = status
    data["SubmissionID"] = submissionID
    data["SubmissionTime"] = submissionTime
    data["SubmissionBy"] = submissionBy
    data["ProblemID"] = problemID
    data["Language"] = language

    response = Response(json.dumps(data))

    return response

@app.route("/logout", methods=["POST"])
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

@app.route("/profile/<name>", methods=["GET", "POST"])
def returnProfilePageWithName(name):
    index_html = open("/opt/nuoj/html/profile.html", "r")
    if request.method == "GET":
        return index_html
    response_data = {}
    profile_data = {}
    code = 200
    conn = connect_mysql()
    try:
        with conn.cursor() as cursor:
            command = "select username, email, admin from `user` where username=%s"
            cursor.execute(command, name)
            result = cursor.fetchone()
            profile_data["username"] = str(result[0])
            profile_data["email"] = str(result[1])
            if(int(result[2]) == 1):
                profile_data["identity"] = "站務管理員"
            else:
                profile_data["identity"] = "會員"
            response_data["status"] = "OK"
            response_data["data"] = profile_data
    except Exception as ex:
        response_data["status"] = "Failed"
        response_data["message"] = "找不到使用者"
        code = 500
    response = Response(json.dumps(response_data), status=code)
    return response

if __name__ == "__main__":
    
    # Initilize isolate
    init_isolate()
    # Initilize mariadb
    conn = connect_mysql()
    
    app.debug = True
    app.run(host="0.0.0.0", port=80)
