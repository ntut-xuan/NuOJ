from flask import *
import time
import os
import auth_util
import database_util
from error_code import error_dict, ErrorCode
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
		session[sessionID] = {"handle": result["data"]["handle"], "email": result["data"]["email"]}

	return resp

@auth.route("/register", methods=["GET", "POST"])
def returnRegisterPage():
	settingJsonObject = json.loads(open("/opt/nuoj/setting.json", "r").read())
	githubStatus = settingJsonObject["oauth"]["github"]["enable"]
	googleStatus = settingJsonObject["oauth"]["google"]["enable"]
	github_client_id = settingJsonObject["oauth"]["github"]["client_id"]
	google_client_id = settingJsonObject["oauth"]["google"]["client_id"]
	google_redirect_url = settingJsonObject["oauth"]["google"]["redirect_url"]

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
		session[sessionID] = {"handle": result["data"]["handle"], "email": result["data"]["email"]}
	else:
		verification_code_dict[verification_code] = result["data"]["handle"]

	return resp

@auth.route("/mail_verification", methods=["GET"])
def mail_verification():

	if "vericode" not in request.args:
		return render_template("mail_check_complete.html", message="驗證失敗，驗證連結需要驗證碼。")

	verification_code = request.args["vericode"]

	if verification_code not in verification_code_dict:
		return render_template("mail_check_complete.html", message="驗證失敗，驗證碼無效。")

	handle = verification_code_dict[verification_code]
	database_util.command_execute("UPDATE `user` SET `email_verified`=1 WHERE handle=%s", (handle))

	del verification_code_dict[verification_code]
	return render_template("mail_check_complete.html", message="驗證成功！")

@auth.route("/mail_check", methods=["GET"])
def mail_check_page():
	return render_template("mail_check.html", **locals())

@auth.route("/handle-setup", methods=["GET", "POST"])
def handle_setup():

	handle_setup_cookie = request.cookies.get("HS")
	email = None
	
	if handle_setup_cookie in session:
		email = session[handle_setup_cookie]["email"]

	if email == None:
		return redirect("/")

	handle_exist = auth_util.handle_exist(email)

	if request.method == "POST":
		result = None
		
		if not handle_exist:
			result = auth_util.handle_setup(request.json, email)
		else:
			result = error_dict(ErrorCode.HANDLE_EXIST)
		
		resp = Response(json.dumps(result), mimetype="application/json")

		if result["status"] == "OK":
			sessionID = os.urandom(16).hex()
			resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
			session[sessionID] = {"handle": result["data"]["handle"], "email": result["data"]["email"]}

		return resp
		
	if handle_exist:
		return redirect("/")

	return render_template("handle_setup.html", **locals())