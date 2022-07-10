from flask import *
import auth_util
import time
import os
import database
from error_code import *

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
	settingJsonObject = json.loads(open("/opt/nuoj/setting.json", "r").read())
	githubStatus = settingJsonObject["oauth"]["github"]["enable"]
	googleStatus = settingJsonObject["oauth"]["google"]["enable"]
	verifyStatus = settingJsonObject["mail"]["enable"]

	if request.method == "GET":
		return render_template("register.html", **locals())

	data = request.json

	result = auth_util.register_db(data)

	if result["status"] == "Failed":
		return Response(json.dumps(result), mimetype="application/json")

	verification_code = result["verification_code"]
	del result["verification_code"]
	
	resp = Response(json.dumps(result), mimetype="application/json")

	if verifyStatus == False:
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
		return error_dict(ErrorCode.REQUIRE_PAPRMETER)

	verification_code = request.args["vericode"]

	if verification_code not in verification_code_dict:
		return error_dict(ErrorCode.EMAIL_VERIFICATION_FAILED)

	username = verification_code_dict[verification_code]
	put_data_str = json.dumps({"email_verification": True})
	resp = database.put_data(("/users/%s" % username), {}, put_data_str)
	
	return Response(json.dumps(resp), mimetype="application/json")

@auth.route("/mail_check", methods=["GET"])
def mail_check_page():
	return render_template("mail_check.html", **locals())