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
import add_problem

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
    count = 0

    # Fetch data
    username = jsonObject["login"]
    email = jsonObject["email"]

    if(email == None):
        email = "github" + str(jsonObject["id"]) + "@github.noreply.com"

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) from `user` where username=%s", jsonObject["login"])
            count = cursor.fetchone()[0]
            cursor.close()
    except Exception as e:
        data["status"] = "Failed"
        data["message"] = str(e)
        return data

    if count == 0:
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO `user` (username, email, password, admin) values (%s, %s, %s, 0)", (username, email, os.urandom(16).hex()))
                conn.commit()
                cursor.close()
        except Exception as e:
            data["status"] = "Failed"
            data["message"] = str(e)
            return data
    
    data["user"] = username
    data["email"] = email

    return data
