from flask import *
import database
import os

problem = Blueprint("problem", __name__)

@problem.route("/add_problem", methods=["GET", "POST"])
def returnAddProblemPage():

	SID = request.cookies.get("SID")

	if(SID not in session):
		return redirect("/")

	data = session[SID]
	username = data["username"]

	n = len(database.get_data("/problems/", {})["data"])

	data_dict = {"problem_pid": os.urandom(10).hex(), "problem_author": username, "index": n+1}

	database.post_data("/problems/", {}, json.dumps(data_dict))
	return redirect("/edit_problem/" + data_dict["problem_pid"] + "/basic")


@problem.route("/edit_problem/<PID>/", methods=["GET", "POST"])
@problem.route("/edit_problem/<PID>/basic", methods=["GET", "POST"])
def returnEditProblemPage(PID):
	
	SID = request.cookies.get("SID")

	if(SID not in session):
		return redirect("/")

	data = session[SID]
	username = data["username"]

	if(request.method == "GET"):
		print(PID)
		response = database.get_data("/problems/%s/" % (PID), {})

		print(response)

		if response["status"] == "Failed":
			return redirect("/")

		problem_data = response["data"]

		if(username != problem_data["problem_author"]):
			return redirect("/")

		title = ""
		description = ""
		input = ""
		output = ""
		note = ""
		memory_limit = ""
		time_limit = ""
		permission = ""

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
	response = database.post_data("/problems/%s/" % (PID), {}, json.dumps(problem_data))
	
	if response["status"] == "Failed":
		return Response(json.dumps({"status": "Failed", "message": response["message"]}))

	return Response(json.dumps({"status": "OK"}))

@problem.route("/edit_problem/<PID>/solution", methods=["GET", "POST"])
def return_solution_page(PID):
    return render_template("add_problem_solution.html", **locals())