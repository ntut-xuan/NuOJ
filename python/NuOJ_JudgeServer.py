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
import traceback
import requests
import add_problem
import codecs
import base64

app = Flask(__name__)

def GenerateData(boxID, dataName, data):
    path = "/var/local/lib/isolate/" + boxID + "/box/"
    dataPath = path + dataName
    metaFilePath = path + "metafile.m"

    # Write File
    f = codecs.open(dataPath, "w+", "UTF-8")
    f.write(data.decode("utf8"))
    f.close()

    subprocess.call("touch " + metaFilePath, shell=True)
    subprocess.call("chmod 777 " + metaFilePath, shell=True)

    run_command = "/usr/bin/g++ %s -o %s" % (dataName, "pre.o")
    command = "isolate --time=2 -p --full-env --meta=\"%s\" --silent --run -- %s" % (metaFilePath, run_command)

    print(command)

    subprocess.call(command, shell=True)

    f = open(metaFilePath, "r")
    meta = f.read().split("\n")

    result = {"status": "OK", "result": {}}

    for info in meta:
        if(":" not in info):
            continue
        
        result["result"][info.split(":")[0]] = info.split(":")[1]
    
    if("status" in result["result"]):
        result["status"] = "Failed"
    
    return result

@app.route("/", methods=["POST"])
def CodePost():
    jsonObjectData = request.json

    box = jsonObjectData["box"]
    language = jsonObjectData["language"]
    code = base64.b64decode(jsonObjectData["code"])
    type = jsonObjectData["type"]
    secret = jsonObjectData["secret"]

    result = {"status": "OK"}

    try:

        if(type == "pre-compile"):
            result = GenerateData(box, "pre.cpp", code)

    except Exception as e:
        traceback.print_exc()
        result["status"] = "Failed"
        result["message"] = str(e)

    return Response(json.dumps(result), mimetype="application/json")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="4433")