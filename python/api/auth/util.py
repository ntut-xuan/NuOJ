#!/usr/bin/env python3
from flask import *
import os
import json
import hashlib
import re
import smtplib
import threading
import jwt
import database_util
import crypto_util as crypto_util
from datetime import *
from tunnel_code import TunnelCode
import setting_util as setting_util
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from error_code import ErrorCode, error_dict

from dataclasses import dataclass

from sqlalchemy.sql import or_, and_
from database import db
from models import User, Profile


@dataclass
class LoginPayload:
    account: str
    password: str


@dataclass
class RegisterPayload:
    email: str
    handle: str
    password: str


def password_cypto(password) -> str:
    m = hashlib.sha256()
    m.update(password.encode("utf8"))
    password = m.hexdigest()
    return password

def login(account: str, password: str) -> bool:
    password = password_cypto(password)

    user: User | None = User.query.filter(and_(or_(User.email == account, User.handle == account), User.password == password)).first()

    if user == None:
        return False
    
    return True

def send_email(email, username, verification_code):

    mail_info = json.loads(open("/etc/nuoj/setting.json", "r").read())["mail"]

    img_file_name = "/etc/nuoj/static/logo_min.png"
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

def register(email: str, handle: str, password: str) -> None:
    # password = crypto_util.Decrypt(password)
    # response = {"status": "OK"}

    # Cypto
    password = password_cypto(password)
    
    # create user_uid
    user_uid = str(uuid4())
    
    # add user
    user: User = User(user_uid=user_uid, email=email, handle=handle, password=password, role=0, email_verified=0)
    db.session.add(user)
    db.session.commit()
    
    # init profile
    profile: Profile = Profile(user_uid=user_uid)
    db.session.add(profile)
    db.session.commit()
    
    # Write into storage (init)
    if not database_util.file_storage_tunnel_exist(user_uid + ".json", TunnelCode.USER_PROFILE):
        database_util.file_storage_tunnel_write(user_uid + ".json", json.dumps({"handle": handle, "email": email, "school": "", "bio": ""}), TunnelCode.USER_PROFILE)

    ''' 
    Temporarity standing off.
    
    # Email verification
    # response["mail_verification_require"] = setting_util.mail_verification_enable()
    # if setting_util.mail_verification_enable() == True:
        # Make email with verification link:
        # verification_code = str(uuid4())
        # response["verification_code"] = verification_code
        # send_email(email, handle, verification_code)
    '''


def handle_exist(email) -> bool:
    result = database_util.command_execute("SELECT handle FROM `user` WHERE email=%s", (email))[0]
    return result["handle"] != None

def handle_setup(data, email) -> dict:

    # User Data
    handle = data["handle"]

    # Validate handle
    handle_valid = bool(re.match("[a-zA-Z\\d](?:[a-zA-Z\\d]|[_-](?=[a-zA-Z\\d])){3,38}$", handle))
    if not handle_valid:
        return error_dict(ErrorCode.HANDLE_INVALID)
    
    # Check handle repeat or not
    result = database_util.command_execute("SELECT COUNT(*) FROM `user` WHERE handle=%s", (handle))[0]
    if result["COUNT(*)"] > 0:
        return error_dict(ErrorCode.HANDLE_REPEAT)

    # Setup Handle
    database_util.command_execute("UPDATE `user` SET handle=%s WHERE email=%s", (handle, email))

    # Setup Handle on storage data
    user_uid = database_util.command_execute("SELECT user_uid from `user` where email=%s", (email))[0]["user_uid"]
    database_util.file_storage_tunnel_write(user_uid + ".json", json.dumps({"handle": handle, "email": email, "school": "", "bio": ""}), TunnelCode.USER_PROFILE)      

    return {"status": "OK", "data": {"email": email, "handle": handle}}

def payload_generator(username, email):
    payload = {"handle": username, "email": email, "iat": datetime.now(tz=timezone.utc), "exp": datetime.now(tz=timezone.utc) + timedelta(days=1)}
    return jwt.encode(payload, "secret", algorithm="HS256")

def jwt_valid(SID):
    return not (SID == None or datetime.now(tz=timezone.utc).timestamp() > jwt.decode(SID, "secret", algorithms=["HS256"])["exp"])

def jwt_decode(SID):
    return jwt.decode(SID, "secret", algorithms=["HS256"])