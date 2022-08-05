#!/usr/bin/env python3
from flask import *
import subprocess
from flask.wrappers import Response
import pymysql
import os
import json
from flask_cors import cross_origin, CORS
from datetime import datetime as dt
from uuid import uuid4
from loguru import logger
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_session import Session
from datetime import timedelta
import time;
import requests
import database_util
from tunnel_code import TunnelCode

def githubLogin(conn, code, settingJsonObject):

    client_id = settingJsonObject["oauth"]["github"]["client_id"]
    client_secret = settingJsonObject["oauth"]["github"]["secret"]
    parameter = {"client_id": client_id, "client_secret": client_secret, "code": code}
    header = {"Accept": "application/json"}
    req = requests.post("https://github.com/login/oauth/access_token", params=parameter, headers=header)
    jsonObject = json.loads(req.text)

    data = {}

    if "access_token" not in jsonObject:
        data["status"] = "Failed"
        data["message"] = "登入失敗"
        return data

    header["Authorization"] = "token " + jsonObject["access_token"]
    req = requests.get("https://api.github.com/user", headers=header)
    jsonObject = json.loads(req.text)
    data["status"] = "OK"

    # Fetch data
    username = jsonObject["login"]
    email = jsonObject["email"]

    if(email == None):
        email = username + "@github.com"

    result = database_util.command_execute("SELECT handle, COUNT(*) from `user` where email=%s", (email))[0]

    if int(result["COUNT(*)"]) == 0:
        user_uid = str(uuid4())
        database_util.command_execute("INSERT INTO `user`(user_uid, password, email, role, email_verified) VALUES(%s, %s, %s, %s, %s)", (user_uid, str(uuid4()), email, 0, True))
        # Write into storage (init, unset handle)
        if not database_util.file_storage_tunnel_exist(user_uid + ".json", TunnelCode.USER_PROFILE):
            database_util.file_storage_tunnel_write(user_uid + ".json", json.dumps({"handle": "", "email": email, "school": "", "bio": ""}), TunnelCode.USER_PROFILE)
    else:
        data["handle"] = result["handle"]

    data["email"] = email

    return data
