from flask import *
import time
import os
import auth_util
import database_util
import setting_util

auth = Blueprint('auth', __name__)

verification_code_dict = {}

@auth.route("/login", methods=["GET", "POST"])
def returnLoginPage():
	settingJsonObject = json.loads(open("/opt/nuoj/setting.json", "r").read())
	githubStatus = settingJsonObject["oauth"]["github"]["enable"]
	googleStatus = settingJsonObject["oauth"]["google"]["enable"]
	github_client_id = settingJsonObject["oauth"]["github"]["client_id"]
	google_client_id = settingJsonObject["oauth"]["google"]["client_id"]
	google_redirect_url = settingJsonObject["oauth"]["google"]["redirect_url"]

	if request.method == "GET":
		return render_template("login.html", **locals())
	
	data = request.json
	result = auth_util.login(data)
	resp = Response(json.dumps(result), mimetype="application/json")

	if(result["status"] == "OK"):
		sessionID = os.urandom(16).hex()
		resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
		session[sessionID] = {"username": result["data"]["username"], "email": result["data"]["email"]}

	return resp

@auth.route("/register", methods=["GET", "POST"])
def returnRegisterPage():

	verifyStatus = setting_util.mail_verification_enable();

	if request.method == "GET":
		return render_template("register.html", **locals())

	data = request.json

	result = auth_util.register_db(data)

	if result["status"] == "Failed":
		return Response(json.dumps(result), mimetype="application/json")

	if setting_util.mail_verification_enable():
		verification_code = result["verification_code"]
		del result["verification_code"]
	
	resp = Response(json.dumps(result), mimetype="application/json")

	if setting_util.mail_verification_enable() == False:
		sessionID = os.urandom(16).hex()
		resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
		session[sessionID] = {"username": result["data"]["username"], "email": result["data"]["email"]}
	else:
		verification_code_dict[verification_code] = result["data"]["username"]

	return resp

@auth.route("/mail_verification", methods=["GET"])
def mail_verification():

	resp = {"status": "OK"}


	if "vericode" not in request.args:
		return render_template("mail_check_complete.html", message="?????????????????????????????????????????????")

	verification_code = request.args["vericode"]

	if verification_code not in verification_code_dict:
		return render_template("mail_check_complete.html", message="?????????????????????????????????")

	username = verification_code_dict[verification_code]
	database_util.command_execute("UPDATE `user` SET `email_verification`=1 WHERE username=%s", (username))

	del verification_code_dict[verification_code]
	return render_template("mail_check_complete.html", message="???????????????")

@auth.route("/mail_check", methods=["GET"])
def mail_check_page():
	return render_template("mail_check.html", **locals())