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

def googleLogin(conn, args, settingJsonObject):
    
    if(args.get("error")):
        data = {"status": "error", "message": args.get("error")}
    else:
        data = {"status": "OK", "result": {"code": args.get("code"), "scope": args.get("scope")}}
    
    code = args.get("code")
    client_id = settingJsonObject["oauth"]["google"]["ID"]
    client_secret = settingJsonObject["oauth"]["google"]["secret"]

    post_data = {"code": code, "client_id": client_id, "client_secret": client_secret, "redirect_uri": "https://nuoj.ntut-xuan.net/google_login", "grant_type": "authorization_code"}

    req = requests.post("https://oauth2.googleapis.com/token", data=post_data)

    jsonObject = json.loads(req.text)

    req = requests.get("https://www.googleapis.com/oauth2/v2/userinfo?access_token=" + jsonObject["access_token"])
    jsonObject = json.loads(req.text)

    email = jsonObject["email"]
    username = jsonObject["name"]

    data = {}
    data["status"] = "OK"

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) from `user` where username=%s", username)
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