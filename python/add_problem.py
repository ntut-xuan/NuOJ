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

def post(data):

    resp = {}

    try:

        problemDirPath = "/opt/nuoj/problem/" + str(data["problemID"])
        problemJsonPath = problemDirPath + "/problem.json"

        if(not os.path.exists(problemDirPath)):
            os.makedirs(problemDirPath)
        
        f = open(problemJsonPath, "w+")
        f.write(json.dumps(data, indent=4))
        f.close()

        resp = {"Status": "OK"}

    except Exception as e:

        resp = {"Status": "Failed", "Exception": str(e)}
    
    return json.dumps(resp)