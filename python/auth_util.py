#!/usr/bin/env python3
from flask import *
import os
import json
import hashlib
import re
import smtplib
import threading
import sys
import database_util as database_util
import setting_util as setting_util
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from error_code import ErrorCode, error_dict

def password_cypto(password) -> str:
    m = hashlib.md5()
    m.update(password.encode("utf8"))
    m.update(m.hexdigest().encode("utf8"))
    password = m.hexdigest()
    return password

def login(data):
    account = data["account"]
    password = password_cypto(data["password"])

    command = "SELECT * FROM `user` WHERE `username` = %s OR `email` = %s;"
    userdata_set = database_util.command_execute(command, (account, account))

    if len(userdata_set) == 0:
        return error_dict(ErrorCode.USERNAME_NOT_FOUND)

    userdata = userdata_set[0]

    if userdata == None or userdata["password"] != password:
        return error_dict(ErrorCode.PASSWORD_NOT_MATCH)
    
    if setting_util.mail_verification_enable() and userdata["email_verification"] == False:
        return error_dict(ErrorCode.EMAIL_NOT_VERIFICATION)

    response_data = {"status": "OK", "data": {"username": userdata["username"], "email": userdata["email"]}}
    return response_data

def send_email(email, username, verification_code):

    mail_info = json.loads(open("/opt/nuoj/setting.json", "r").read())["mail"]

    img_file_name = "/opt/nuoj/static/logo_min.png"
    with open(img_file_name, 'rb') as f:
        img_data = f.read()

    image = MIMEImage(img_data, name=os.path.basename(img_file_name))
    image.add_header('Content-ID', '<{}>'.format(os.path.basename(img_file_name)))

    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "NuOJ 驗證信件"  #郵件標題
    content["from"] = "NuOJ@noreply.me"  #寄件者
    content["to"] = email #收件者
    
    verification_url = mail_info["redirect_url"] + "?vericode=%s" % (verification_code)

    content.attach(image)
    content.attach(MIMEText(render_template("mail_template.html", **locals()), 'html'))  #郵件內容

    def send(mail_info, content):
        with smtplib.SMTP(host=mail_info["server"], port=mail_info["port"]) as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login(mail_info["mailname"], mail_info["password"])  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)

    thread = threading.Thread(target=send, args=[mail_info, content])
    thread.start()

def register_db(data) -> dict:

    # User Data
    email = data["email"]
    username = data["username"]
    password = data["password"]
    admin = 0
    response = {"status": "OK"}

    # Check Data Valid
    username_valid = bool(re.match("^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", username))
    if not username_valid:
        return {"status": "Failed", "message": "Invalid username"}
    
    # Check repeat username
    user_data = database_util.command_execute("SELECT * FROM `user` WHERE `username` = %s", (username))
    if len(user_data):
        return {"status": "Failed", "message": "Repeat Username"}
    
    # Check repeat email
    user_data = database_util.command_execute("SELECT * FROM `user` WHERE `email` = %s", (email))
    if len(user_data):
        return {"status": "Failed", "message": "Repeat Email"}

    # Cypto
    password = password_cypto(password)

    # Write into database
    database_util.command_execute("INSERT INTO `user`(username, password, email, admin, email_verification) VALUES(%s,%s,%s,%s,%s)", (username, password, email, admin, False))
    data_dict = {"user_id": str(uuid4()), "email": email, "username": username, 
                "password": password, "admin": admin, "email_verification": False}

    # Email verification
    mail_info = json.loads(open("/opt/nuoj/setting.json", "r").read())["mail"]
    response["mail_verification_require"] = mail_info["enable"]
    if mail_info["enable"] == True:
        # Make email with verification link:
        verification_code = str(uuid4())
        response["verification_code"] = verification_code
        send_email(email, username, verification_code)

    # Check write result
    response["data"] = data_dict
    return response