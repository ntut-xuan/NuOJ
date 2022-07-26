from flask import *
import time
import os
import auth_util
import database_util
from error_code import error_dict, ErrorCode
import setting_util
from datetime import datetime
from uuid import uuid4
from tunnel_code import TunnelCode

problem_page = Blueprint('problem_page', __name__)

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

@problem_page.route("/submit/", methods=["POST"])
def submitCode():

	# Check session valid
	SID = request.cookies.get("SID")
	login = SID in session

	if not login:
		return Response(json.dumps(error_dict(ErrorCode.REQUIRE_AUTHORIZATION)), mimetype="application.json")

	session_data = session[SID]
	data = request.json
	
	# Create submission infomation
	code = data["code"]
	problem_id = data["problem_id"]
	submission_id = str(uuid4())
	user_uid = database_util.command_execute("SELECT user_uid from `user` WHERE email=%s", (session_data["email"]))[0]["user_uid"]
	language = "C++"
	date = datetime.now()

	# Save code to storage
	database_util.file_storage_tunnel_write(submission_id + ".cpp", code, TunnelCode.SUBMISSION)

	# Save info to SQL
	database_util.command_execute("INSERT INTO `submission`(solution_id, problem_id, user_uid, language, date) VALUE(%s, %s, %s, %s, %s)", (submission_id, problem_id, user_uid, language, date))

	return Response(json.dumps({"status": "OK"}), mimetype="application/json")