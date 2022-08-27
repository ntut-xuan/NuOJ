from importlib.metadata import requires
from flask import *
from tunnel_code import TunnelCode
from auth_util import jwt_decode, jwt_valid
import database_util as database_util
from uuid import uuid4
from functools import wraps
from datetime import datetime
import os
import requests

problem = Blueprint("problem", __name__)

def require_session_or_redirect_index(func):
	@wraps(func)
	def decorator(*args, **kwargs):
		SID = request.cookies.get("SID")
		if not jwt_valid(SID):
			return redirect("/")
		return func(*args, **kwargs)
	return decorator

def session_name_auth(func):
	@wraps(func)
	def decorator(PID):
		SID = request.cookies.get("SID")
		data = jwt_decode(SID)
		username = data["handle"]
		problem_mysql_data = database_util.command_execute("SELECT * from `problem` WHERE problem_pid = %s", (PID))[0]
		problem_storage_raw_data = database_util.file_storage_tunnel_read("%s.json" % PID, TunnelCode.PROBLEM)

		if(username != problem_mysql_data["problem_author"]):
			return redirect("/")
		
		return func(PID)
	return decorator

@problem.route("/add_problem", methods=["GET", "POST"])
@require_session_or_redirect_index
def returnAddProblemPage():

	SID = request.cookies.get("SID")

	data = jwt_decode(SID)
	handle = data["handle"]
	problem_pid = os.urandom(10).hex()

	database_util.command_execute("INSERT INTO `problem`(problem_pid, problem_author) VALUES(%s,%s)", (problem_pid, handle))

	return redirect("/edit_problem/" + problem_pid + "/basic")


@problem.route("/edit_problem/<PID>/", methods=["GET", "POST"])
@problem.route("/edit_problem/<PID>/basic", methods=["GET", "POST"])
@require_session_or_redirect_index
def returnEditProblemPage(PID):
	
	SID = request.cookies.get("SID")
	data = jwt_decode(SID)
	username = data["handle"]

	@session_name_auth
	def get_methods(PID):
		problem_storage_raw_data = database_util.file_storage_tunnel_read("%s.json" % PID, TunnelCode.PROBLEM)

		title = ""
		description = ""
		input = ""
		output = ""
		note = ""
		memory_limit = ""
		time_limit = ""
		permission = ""

		if len(problem_storage_raw_data) != 0:
			problem_data = json.loads(problem_storage_raw_data)
			if "problem_content" in problem_data:
				title = problem_data["problem_content"]["title"]
				description = problem_data["problem_content"]["description"]
				input = problem_data["problem_content"]["input"]
				output = problem_data["problem_content"]["output"]
				note = problem_data["problem_content"]["note"]
				memory_limit = problem_data["basic_setting"]["memory_limit"]
				time_limit = problem_data["basic_setting"]["time_limit"]
				permission = problem_data["basic_setting"]["permission"]
		
		return render_template("add_problem_bs.html", **locals())

	if(request.method == "GET"):
		return get_methods(PID)

	problem_data = json.loads(request.data)
	database_util.file_storage_tunnel_write("%s.json" % (PID), json.dumps(problem_data), TunnelCode.PROBLEM)

	return Response(json.dumps({"status": "OK"}))

@problem.route("/edit_problem/<PID>/solution", methods=["GET", "POST"])
@require_session_or_redirect_index
@session_name_auth
def return_solution_page(PID):
    return render_template("add_problem_solution.html", **locals())

@problem.route("/edit_problem/<PID>/testcase", methods=["GET", "POST"])
@require_session_or_redirect_index
@session_name_auth
def return_testcase_page(PID):
	return render_template("add_problem_testcase.html", **locals())

@problem.route("/edit_problem/<PID>/solution_pre_compile", methods=["GET", "POST"])
@require_session_or_redirect_index
@session_name_auth
def pre_compile(PID):
	# fetch data
	json_post_data = request.json
	jwt_data = jwt_decode(request.cookies.get("SID"))
	code_list = []
	# collect code to list
	for data in json_post_data["data"]:
		code_list.append(data["code"])
	# register into database 
	for code in code_list:
		submission_uuid = str(uuid4())
		problem_id = json_post_data["problem_pid"]
		user_uid = jwt_data["handle"]
		language = "C++"
		date = datetime.now().timestamp()
		submission_type = "PC"
		# Register into SQL
		database_util.command_execute("INSERT `submission`(solution_id, problem_id, user_uid, language, date, type) VALUES(%s, %s, %s, %s, %s, %s)", (submission_uuid, problem_id, user_uid, language, date, submission_type))
		# Storage code to Storage
		database_util.file_storage_tunnel_write(submission_uuid + ".cpp", code, TunnelCode.SUBMISSION)
		# Doing POST to sandbox]
		webhook_url = "https://nuoj.ntut-xuan.net/result_webhook/%s/" % (submission_uuid)
		resp = requests.post("http://localhost:4439/judge", data=json.dumps({"code": code, "execution": "C", "option": {"threading": True, "time": 4, "wall_time": 4, "webhook_url": webhook_url}}), headers={"content-type": "application/json"})
		print(resp.text)
	return Response(json.dumps({"status": "OK"}), mimetype="application/json")


@problem.route("/result_webhook/<submission_uuid>/", methods=["POST"])
def result_webhook(submission_uuid):
	print(submission_uuid, request.json)
	return Response(json.dumps({"status": "OK"}), mimetype="application/json")