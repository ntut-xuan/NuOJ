#!/usr/bin/env python3
from tabnanny import check, verbose
from unicodedata import name
from flask import *
import subprocess
from flask.wrappers import Response
import pymysql
import os
import json
import hashlib
import re
import string
import random
import time
import smtplib
from flask_cors import cross_origin, CORS
from datetime import datetime as dt
from uuid import uuid4
from loguru import logger
from flask_session import Session
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def login(conn, data):
    account = data["account"]
    password = data["password"]
    m = hashlib.md5()
    m.update(password.encode("utf8"))
    m.update(m.hexdigest().encode("utf8"))
    password = m.hexdigest()

    data = {"status": "Failed", "message": "Incorrect account or password"}

    with conn.cursor() as cursor:
        if('@' in account):
            cursor.execute("SELECT email, username FROM `user` WHERE email=%s and password=%s", (account, password))
        else:
            cursor.execute("SELECT email, username FROM `user` WHERE username=%s and password=%s", (account, password))
        result = cursor.fetchone()
        if result != None:
            data["status"] = "OK"
            data["email"] = result[0]
            data["username"] = result[1]
        cursor.close()

    return data

def register(conn, data):
    email = data["email"]
    username = data["username"]
    password = data["password"]
    verify_code = data["verify_code"]

    m = hashlib.md5()
    m.update(password.encode("utf8"))
    m.update(m.hexdigest().encode("utf8"))
    password = m.hexdigest()

    data = {"status": "Failed", "message": ""}


    username_valid = bool(re.match("^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", username))

    print(username_valid)

    if(username_valid != True):
        data["message"] = "Invalid username"
        return data

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM `user` WHERE email=%s", (email))
        result = cursor.fetchone()
        if result != None:
            data["message"] = "Repeat Email"
            cursor.close()
            return data
        cursor.close()

    print("OK")
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM `user` WHERE username=%s", (username))
        result = cursor.fetchone()
        if result != None:
            data["message"] = "Repeat Username"
            cursor.close()
            return data
        cursor.close()

  
    VerifyCodeObject = json.loads(open("/tmp/verify_code", "r").read())

    print(data)
    
    if username in VerifyCodeObject:
        VerifyCodeUser = VerifyCodeObject[username]
        
        if VerifyCodeUser['time'] - time.time() > 600:
            data["status"] = "TimeOut"
            data["username"] = username
            data["email"] = email

            return data

        if VerifyCodeUser['code'] != verify_code:
            data["status"] = "WrongCode"
            data["username"] = username
            data["email"] = email
        
            return data
        
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO `user` (username, email, password, admin) values (%s, %s, %s, 0)", (username, email, password))
            conn.commit()
            cursor.close()
        
        data["status"] = "OK"
        data["username"] = username
        data["email"] = email

    return data

def VerifyCode(conn, data):
    mail_info = json.loads(open("/opt/nuoj/setting.json", "r").read())["mail"]
    email = data["email"]
    username = data["username"]
    password = data["password"]

    m = hashlib.md5()
    m.update(password.encode("utf8"))
    m.update(m.hexdigest().encode("utf8"))
    password = m.hexdigest()

    data = {"status": "Failed", "message": ""}


    username_valid = bool(re.match("^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", username))

    print(username_valid)

    if(username_valid != True):
        data["message"] = "Invalid username"
        return data

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM `user` WHERE email=%s", (email))
        result = cursor.fetchone()
        if result != None:
            data["message"] = "Repeat Email"
            cursor.close()
            return data
        cursor.close()

    print("OK")
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM `user` WHERE username=%s", (username))
        result = cursor.fetchone()
        if result != None:
            data["message"] = "Repeat Username"
            cursor.close()
            return data
        cursor.close()

    VerifyCodeObject = json.loads(open("/tmp/verify_code", "r").read())
    verify_code = {}
    verify_code['time'] = time.time()
    verify_code['code'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    VerifyCodeObject[username] = verify_code

    file = open("/tmp/verify_code", "w")
    json.dump(VerifyCodeObject, file)
    file.close()

    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "NuOJ驗證信件"  #郵件標題
    content["from"] = "Mail Authentication"  #寄件者
    content["to"] = email #收件者
    content.attach(MIMEText(verify_code['code']))  #郵件內容

    with smtplib.SMTP(host=mail_info["server"], port=mail_info["port"]) as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(mail_info["mailname"], mail_info["password"])  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
    
    data['status'] = "OK"

    return data