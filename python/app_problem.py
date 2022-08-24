import traceback
from flask import *
import time
import os
import auth_util
import database_util
from error_code import error_dict, ErrorCode
import setting_util
from auth_util import jwt_decode, jwt_valid
from datetime import datetime
from uuid import uuid4
from tunnel_code import TunnelCode
from functools import wraps

problem_page = Blueprint('problem_page', __name__)

def require_session(func):
	@wraps(func)
	def decorator(*args, **kwargs):

		SID = request.cookies.get("SID")

		if not jwt_valid(SID):
			resp = Response(json.dumps(error_dict(ErrorCode.REQUIRE_AUTHORIZATION)), mimetype="application/json")
			resp.set_cookie("SID", value = "", expires=0)
			return resp
		
		return func(*args, **kwargs)
	return decorator

@problem_page.route("/problem/<int:ID>", methods=["GET", "POST"])
def returnProblemIDPage(ID):
	problem_pid = database_util.command_execute("SELECT problem_pid FROM `problem` WHERE `ID` = %s", (ID))[0]["problem_pid"]
	problemJsonObject = json.loads(database_util.file_storage_tunnel_read(problem_pid + ".json", TunnelCode.PROBLEM))
	title = problemJsonObject["problem_content"]["title"]
	description = problemJsonObject["problem_content"]["description"].split("\n")
	input_description = problemJsonObject["problem_content"]["input"].split("\n")
	output_description = problemJsonObject["problem_content"]["output"].split("\n")
	note = problemJsonObject["problem_content"]["note"].split("\n")
	TL = problemJsonObject["basic_setting"]["time_limit"]
	ML = problemJsonObject["basic_setting"]["memory_limit"]
	return render_template("problem_page.html", **locals())

@problem_page.route("/submit", methods=["POST"])
@require_session
def submitCode():

	try:
		SID = request.cookies.get("SID")
		session_data = jwt_decode(SID)
		data = request.json
		
		# Create submission infomation
		code = data["code"]
		problem_id = data["problem_id"]
		submission_id = str(uuid4())
		user_uid = database_util.command_execute("SELECT user_uid FROM `user` WHERE email=%s", (session_data["email"]))[0]["user_uid"]
		language = "C++"
		date = datetime.now()

		# Check problem exist
		problem_count = database_util.command_execute("SELECT COUNT(*) FROM `problem` WHERE ID=%s", (data["problem_id"]))[0]["COUNT(*)"]
		
		if problem_count == 0:
			return Response(json.dumps(error_dict(ErrorCode.INVALID_DATA)), mimetype="application/json")

		# Save code to storage
		database_util.file_storage_tunnel_write(submission_id + ".cpp", code, TunnelCode.SUBMISSION)

		# Save info to SQL
		database_util.command_execute("INSERT INTO `submission`(solution_id, problem_id, user_uid, language, date) VALUE(%s, %s, %s, %s, %s)", (submission_id, problem_id, user_uid, language, date))

		return Response(json.dumps({"status": "OK"}), mimetype="application/json")

	except Exception as e:
		return Response(json.dumps(error_dict(ErrorCode.UNEXCEPT_ERROR)), mimetype="application/json")


@problem_page.route("/problem_page_num")
@require_session
def getProblemNum():
	try:	
		SID = request.cookies.get("SID")
		handle = jwt_decode(SID)["handle"]
	except:
		return "please login", 400

	count = database_util.command_execute("select count(*) from problem")
	response={
		"count":count[0]["count(*)"]
	}
	return response


@problem_page.route("/all_problem_list")
@require_session
def getAllProblemList():
	try:	
		SID = request.cookies.get("SID")
		handle = jwt_decode(SID)["handle"]
	except:
		return "please login", 400
	
	args = request.args
	number_of_problem = int(args["numbers"])
	offset = int(args["from"])

	problems = database_util.command_execute("select * from problem limit %s offset %s;",(number_of_problem,offset))
	result =[]
	i=0
	for problem in problems:
		problem_pid = problem["problem_pid"]
		problem_raw_data = database_util.file_storage_tunnel_read("%s.json"%problem_pid,TunnelCode.PROBLEM)

		if( len(problem_raw_data)!= 0):

			problem_json = json.loads(problem_raw_data)

			permission = False

			if(problem_json["basic_setting"]["permission"] == "1"):
				permission = True
			
			subdata = {"id":problem["ID"], "title" : problem_json["problem_content"]["title"], "permission" :	permission , "author" : problem["problem_author"], "problem_pid":problem_pid , "tag":[]}
			result.append(subdata)
			i+=1
	return {"data":result}