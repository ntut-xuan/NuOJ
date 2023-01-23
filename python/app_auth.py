import time
import os
import auth_util
import jwt
import database_util
import setting_util
import github_login_util
import google_login_util
from auth_util import jwt_decode, jwt_valid, payload_generator
from datetime import timedelta, datetime, timezone
from flask import *
from error_code import error_dict, ErrorCode

auth = Blueprint('auth', __name__)

verification_code_dict = {}

@auth.route("/session_verification", methods=["POST"])
def session_veri():
	SID = request.cookies.get("SID")
	if not jwt_valid(SID):
		resp = Response(json.dumps(error_dict(ErrorCode.REQUIRE_AUTHORIZATION)), mimetype="application/json")
		resp.set_cookie("SID", value="", expires=0)
		return resp

	return Response(json.dumps({"status": "OK", "handle": jwt_decode(SID)["handle"]}), mimetype="application/json")

@auth.route("/oauth_info", methods=["GET"])
def oauth_info():
	github_status = setting_util.github_oauth_enable()
	google_status = setting_util.github_oauth_enable()
	github_client_id = setting_util.github_oauth_client_id()
	google_client_id = setting_util.google_oauth_client_id()
	google_redirect_url = setting_util.google_oauth_redirect_url()
	google_oauth_scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"

	response = {"status": "OK"}

	if github_status:
		response["github_oauth_url"] = "https://github.com/login/oauth/authorize?client_id=%s&scope=repo" % (github_client_id) 

	if google_status:
		response["google_oauth_url"] = "https://accounts.google.com/o/oauth2/v2/auth?client_id=%s&redirect_uri=%s&response_type=code&scope=%s" % (google_client_id, google_redirect_url, google_oauth_scope)

	return Response(json.dumps(response), mimetype="application/json")

@auth.route("/login", methods=["GET", "POST"])
def returnLoginPage():

	if request.method == "GET":
		return render_template("login.html", **locals())
	
	data = request.json
	result = auth_util.login(data)
	resp = Response(json.dumps(result), mimetype="application/json")

	if(result["status"] == "OK"):
		sessionID = payload_generator(result["data"]["handle"], result["data"]["email"])
		resp.set_cookie("SID", value = sessionID, expires=(datetime.now(tz=timezone.utc) + timedelta(days=1)).timestamp())

	return resp

@auth.route("/register", methods=["GET", "POST"])
def returnRegisterPage():
	if request.method == "GET":
		return render_template("register.html", **locals())

	data = request.json

	result = auth_util.register_db(data)

	if result["status"] == "Failed":
		return Response(json.dumps(result), mimetype="application/json")

	if setting_util.mail_verification_enable():
		verification_code = result["verification_code"]
		result["mail_verification_redirect"] = True
		del result["verification_code"]
	else:
		result["mail_verification_redirect"] = False

	resp = Response(json.dumps(result), mimetype="application/json")

	if setting_util.mail_verification_enable() == False:
		sessionID = payload_generator(result["data"]["handle"], result["data"]["email"])
		resp.set_cookie("SID", value = sessionID, expires=time.time()+24*60*60)
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

@auth.route("/github_login", methods=["GET", "POST"])
def processGithubLogin():
	
	settingJsonObject = json.loads(open("/etc/nuoj/setting.json", "r").read())
	data = github_login_util.githubLogin(request.args.get("code"), settingJsonObject)

	if(data["status"] == "OK"):
		if "handle" not in data or data["handle"] == None:
			resp = redirect("/handle-setup")
			sessionID = os.urandom(16).hex()
			resp.set_cookie("HS", value = sessionID, expires=time.time()+24*60*60)
			session[sessionID] = {"email": data["email"]}
		else:
			resp = redirect("/")
			jwt_cookie = auth_util.payload_generator(data["handle"], data["email"])
			resp.set_cookie("SID", value = jwt_cookie, expires=time.time()+24*60*60)
		return resp
	else:
		return Response(json.dumps(data), mimetype="application/json")

@auth.route("/google_login", methods=["GET", "POST"])
def processGoogleLogin():

	settingJsonObject = json.loads(open("/etc/nuoj/setting.json", "r").read())
	data = google_login_util.googleLogin(request.args, settingJsonObject)
	resp = None

	if(data["status"] == "OK"):
		if "handle" not in data or data["handle"] == None:
			resp = redirect("/handle-setup")
			sessionID = os.urandom(16).hex()
			resp.set_cookie("HS", value = sessionID, expires=time.time()+24*60*60)
			session[sessionID] = {"email": data["email"]}
		else:
			resp = redirect("/")
			jwt_cookie = auth_util.payload_generator(data["handle"], data["email"])
			resp.set_cookie("SID", value = jwt_cookie, expires=time.time()+24*60*60)
		return resp
	else:
		return Response(json.dumps(data), mimetype="application/json")

@auth.route("/veriCookie")
def veriCookie(cookie):
	data = {}
	if cookie in session:
		data["status"] = "OK"
		data["result"] = {"cookie": session[cookie]}
	else:
		data["status"] = "Failed"
	return json.dumps(data)

@auth.route("/pubkey")
def pubkey():
	return send_from_directory('../', "public.pem")

@auth.route("/logout", methods=["GET", "POST"])
def logout():
	resp = Response(json.dumps({"status": "OK"}))
	resp.set_cookie("SID", value = "", expires=0)
	return resp