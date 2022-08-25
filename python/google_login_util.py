#!/usr/bin/env python3
from flask import *
import os
import json
import requests
import database_util
from uuid import uuid4
from tunnel_code import TunnelCode

def googleLogin(args, settingJsonObject):
    
    if(args.get("error")):
        data = {"status": "error", "message": args.get("error")}
    else:
        data = {"status": "OK", "result": {"code": args.get("code"), "scope": args.get("scope")}}
    
    code = args.get("code")
    client_id = settingJsonObject["oauth"]["google"]["client_id"]
    client_secret = settingJsonObject["oauth"]["google"]["secret"]

    post_data = {"code": code, "client_id": client_id, "client_secret": client_secret, "redirect_uri": "https://nuoj.ntut-xuan.net/google_login", "grant_type": "authorization_code"}

    req = requests.post("https://oauth2.googleapis.com/token", data=post_data)

    jsonObject = json.loads(req.text)

    req = requests.get("https://www.googleapis.com/oauth2/v2/userinfo?access_token=" + jsonObject["access_token"])
    jsonObject = json.loads(req.text)

    email = jsonObject["email"]

    data = {}
    data["status"] = "OK"

    result = database_util.command_execute("SELECT COUNT(*) FROM `user` WHERE email=%s", (email))[0]
    count = result["COUNT(*)"]

    if count == 0:
        user_uid = str(uuid4())
        database_util.command_execute("INSERT INTO `user`(user_uid, password, email, role, email_verified) VALUES(%s, %s, %s, %s, %s)", (user_uid, str(uuid4()), email, 0, True))
        if not database_util.file_storage_tunnel_exist(user_uid + ".json", TunnelCode.USER_PROFILE):
            database_util.file_storage_tunnel_write(user_uid + ".json", json.dumps({"handle": "", "email": email, "school": "", "bio": ""}), TunnelCode.USER_PROFILE)
    else:
        result = database_util.command_execute("SELECT handle FROM `user` WHERE email=%s", (email))[0]
        data["handle"] = result["handle"]

    data["email"] = email

    return data