from flask import *
from tunnel_code import TunnelCode
import database_util as database_util
import os

problem = Blueprint("problem", __name__)

@problem.route("/add_problem", methods=["GET", "POST"])
def returnAddProblemPage():

	SID = request.cookies.get("SID")

	if(SID not in session):
		return redirect("/")

	data = session[SID]
	username = data["username"]
	problem_pid = os.urandom(10).hex()

	database_util.command_execute("INSERT INTO `problem`(problem_pid, problem_author) VALUES(%s,%s)", (problem_pid, username))
	return redirect("/edit_problem/" + problem_pid + "/basic")


@problem.route("/edit_problem/<PID>/", methods=["GET", "POST"])
@problem.route("/edit_problem/<PID>/basic", methods=["GET", "POST"])
def returnEditProblemPage(PID):
	
	SID = request.cookies.get("SID")

	if(SID not in session):
		return redirect("/")

	data = session[SID]
	username = data["username"]

	if(request.method == "GET"):

		problem_mysql_data = database_util.command_execute("SELECT * from `problem` WHERE problem_pid = %s", (PID))[0]
		problem_storage_raw_data = database_util.file_storage_tunnel_read("%s.json" % PID, TunnelCode.PROBLEM)

		if(username != problem_mysql_data["problem_author"]):
			return redirect("/")

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

	problem_data = json.loads(request.data)
	database_util.file_storage_tunnel_write("%s.json" % (PID), json.dumps(problem_data), TunnelCode.PROBLEM)

	return Response(json.dumps({"status": "OK"}))

@problem.route("/edit_problem/<PID>/solution", methods=["GET", "POST"])
def return_solution_page(PID):
    return render_template("add_problem_solution.html", **locals())