from importlib.metadata import requires
from flask import *
from tunnel_code import TunnelCode
from auth_util import jwt_decode, jwt_valid
from error_code import error_dict, ErrorCode
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
def pre_compile_and_save(PID):
	# fetch data
	json_post_data = request.json
	jwt_data = jwt_decode(request.cookies.get("SID"))
	solution_group = uuid4()
	problem_id = json_post_data["problem_pid"]
	# register new solution_group to database
	database_util.command_execute("UPDATE problem SET solution_group=%s WHERE problem_pid=%s", (solution_group, problem_id))
	# register every code into database 
	for code_data in json_post_data["data"]:
		submission_uuid = str(uuid4())
		user_uid = jwt_data["handle"]
		language = "C++"
		date = datetime.now()
		submission_type = "PC"
		# Register into SQL
		database_util.command_execute("INSERT `submission`(solution_id, problem_id, user_uid, language, date, type, solution_group) VALUES(%s, %s, %s, %s, %s, %s, %s)", (submission_uuid, problem_id, user_uid, language, date, submission_type, solution_group))
		# Storage code to Storage
		database_util.file_storage_tunnel_write(submission_uuid + ".cpp", code_data["code"], TunnelCode.SOLUTION)
		# Doing POST to sandbox
		webhook_url = "https://nuoj.ntut-xuan.net/compile_result_webhook/%s/" % (submission_uuid)
		requests.post("http://localhost:4439/judge", data=json.dumps({
			"code": code_data["code"], 
			"execution": "C",
			"code_language": "cpp",
			"option": {"threading": True, "time": 4, "wall_time": 4, "webhook_url": webhook_url}}), headers={"content-type": "application/json"})
	return Response(json.dumps({"status": "OK"}), mimetype="application/json")

@problem.route("/fetch_solutions/<PID>", methods=["GET"])
def fetch_solution(PID):
	# fetch solution_group
	solution_group = database_util.command_execute("SELECT solution_group from `problem` WHERE problem_pid=%s", (PID))[0]["solution_group"]
	# fetch submissions status
	submissions = database_util.command_execute("SELECT * FROM `submission` WHERE solution_group=%s", (solution_group))
	complie_status = "Finish"
	solution_group_data = []
	for submission in submissions:
		solution_id = submission["solution_id"]
		code = database_util.file_storage_tunnel_read(solution_id + ".cpp", TunnelCode.SOLUTION)
		result = database_util.command_execute("SELECT result FROM `submission` WHERE solution_id=%s", (solution_id))[0]["result"]
		if result == "" or result == None:
			complie_status = "Running"
		solution_group_data.append({"code": code, "result": result, "uuid": solution_id})
	return Response(json.dumps({"status": "OK", "compile_status": complie_status, "data": solution_group_data}), mimetype="application/json")

@problem.route("/compile_result_webhook/<submission_uuid>/", methods=["POST"])
def result_webhook(submission_uuid):
	# Check submission uuid exists
	count = database_util.command_execute("SELECT COUNT(*) FROM `submission` WHERE solution_id=%s", (submission_uuid))[0]["COUNT(*)"]
	if count == 0:
		return Response(json.dumps(error_dict(ErrorCode.INVALID_DATA, "submission_uuid not exist.")), mimetype="application/json")
	resp_data = request.json
	if resp_data["status"] != "OK":
		return Response(json.dumps(error_dict(ErrorCode.UNEXCEPT_ERROR)), mimetype="application/json")
	compile_result_data = resp_data["data"]["result"]
	compile_result = compile_result_data["compile-result"]
	compile_time = compile_result_data["time"]
	compile_memory = "%.2f" % (float(compile_result_data["cg-mem"]) / 1024)
	database_util.command_execute("UPDATE submission SET result=%s, time=%s, memory=%s WHERE solution_id=%s", (compile_result, compile_time, compile_memory, submission_uuid))
	return Response(json.dumps({"status": "OK"}), mimetype="application/json")