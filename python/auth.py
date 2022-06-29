#!/usr/bin/env python3
from flask import *
import subprocess
from flask.wrappers import Response
import pymysql
import os
import json
import hashlib
import re
from flask_cors import cross_origin, CORS
from datetime import datetime as dt
from uuid import uuid4
from loguru import logger
from flask_session import Session
from datetime import timedelta

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

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO `user` (username, email, password, admin) values (%s, %s, %s, 0)", (username, email, password))
        conn.commit()
        cursor.close()


    data["status"] = "OK"
    data["username"] = username
    data["email"] = email
    return data