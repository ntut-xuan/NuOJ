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

    # Check Data Valid
    if '@' in account:
        email_valid = bool(re.match("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", account))
        if not email_valid:
            return error_dict(ErrorCode.EMAIL_INVALID)
    else:
        handle_valid = bool(re.match("[a-zA-Z\d](?:[a-zA-Z\d]|_(?=[a-zA-Z\d])){0,38}$", account))
        if not handle_valid:
            return error_dict(ErrorCode.HANDLE_INVALID)

    password_valid = bool(re.match("(?=.*?[a-zA-Z])(?=.*?[0-9]).{8,}$", password))
    if not password_valid:
        return error_dict(ErrorCode.PASSWORD_INVALID)

    command = "SELECT * FROM `user` WHERE `handle` = %s OR `email` = %s;"
    userdata_set = database_util.command_execute(command, (account, account))

    if len(userdata_set) == 0:
        return error_dict(ErrorCode.HANDLE_NOT_FOUND)

    userdata = userdata_set[0]

    if userdata == None or userdata["password"] != password:
        return error_dict(ErrorCode.PASSWORD_NOT_MATCH)
    
    if setting_util.mail_verification_enable() and userdata["email_verified"] == False:
        return error_dict(ErrorCode.EMAIL_NOT_VERIFICATION)

    response_data = {"status": "OK", "data": {"handle": userdata["handle"], "email": userdata["email"]}}
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
    handle = data["handle"]
    password = data["password"]
    admin = 0
    response = {"status": "OK"}

    # Check Data Valid
    handle_valid = bool(re.match("[a-zA-Z\d](?:[a-zA-Z\d]|_(?=[a-zA-Z\d])){0,38}$", handle))
    if not handle_valid:
        return error_dict(ErrorCode.HANDLE_INVALID)
    
    email_valid = bool(re.match("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email))
    if not email_valid:
        return error_dict(ErrorCode.EMAIL_INVALID)

    password_valid = bool(re.match("(?=.*?[a-zA-Z])(?=.*?[0-9]).{8,}$", password))
    if not password_valid:
        return error_dict(ErrorCode.PASSWORD_INVALID)

    # Check repeat username
    user_data = database_util.command_execute("SELECT * FROM `user` WHERE `handle` = %s", (handle))
    if len(user_data):
        return error_dict(ErrorCode.HANDLE_EXIST)
    
    # Check repeat email
    user_data = database_util.command_execute("SELECT * FROM `user` WHERE `email` = %s", (email))
    if len(user_data):
        return error_dict(ErrorCode.EMAIL_EXIST)

    # Cypto
    password = password_cypto(password)

    # Write into database
    user_uid = str(uuid4())
    database_util.command_execute("INSERT INTO `user`(user_uid, handle, password, email, role, email_verified) VALUES(%s, %s, %s, %s, %s, %s)", (user_uid, handle, password, email, admin, False))
    data_dict = {"user_id": user_uid, "email": email, "handle": handle, 
                "password": password, "admin": admin, "email_verified": False}

    # Email verification
    mail_info = json.loads(open("/opt/nuoj/setting.json", "r").read())["mail"]
    response["mail_verification_require"] = mail_info["enable"]
    if mail_info["enable"] == True:
        # Make email with verification link:
        verification_code = str(uuid4())
        response["verification_code"] = verification_code
        send_email(email, handle, verification_code)

    # Check write result
    response["data"] = data_dict
    return response

def handle_exist(email) -> bool:
    result = database_util.command_execute("SELECT handle FROM `user` WHERE email=%s", (email))[0]
    return result["handle"] != None

def handle_setup(data, email) -> dict:

    # User Data
    handle = data["handle"]

    # Validate handle
    handle_valid = bool(re.match("^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", handle))
    if not handle_valid:
        return error_dict(ErrorCode.HANDLE_INVALID)
    
    # Check handle repeat or not
    result = database_util.command_execute("SELECT COUNT(*) FROM `user` WHERE handle=%s", (handle))[0]
    if result["COUNT(*)"] > 0:
        return error_dict(ErrorCode.HANDLE_REPEAT)

    # Setup Handle
    database_util.command_execute("UPDATE `user` SET handle=%s WHERE email=%s", (handle, email))

    return {"status": "OK", "data": {"email": email, "handle": handle}}