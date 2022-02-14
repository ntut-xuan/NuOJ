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
import codecs

def post(conn, data):

	resp = {}

	try:

		''' add file to file dic '''

		problemDirPath = "/opt/nuoj/problem/" + str(data["problemID"])
		problemJsonPath = problemDirPath + "/problem.json"

		if(not os.path.exists(problemDirPath)):
			os.makedirs(problemDirPath)

		jsonObject = data
		
		f = codecs.open(problemJsonPath, "w+", "UTF-8")
		f.write(json.dumps(data, indent=4, ensure_ascii=False))
		f.close()

		''' SQL '''

		try:
			with conn.cursor() as cursor:
				command = "INSERT `problem`(name, visibility, author) VALUES (%s, %s, %s)" % (str(jsonObject["problemContent"]["title"]), str(jsonObject["basicSetting"]["permission"]), "null")
				cursor.execute(command)
				conn.commit()
				cursor.close()
				conn.close()
		except Exception as ex:
			logger.error(ex)

		resp = {"Status": "OK"}

	except Exception as e:

		resp = {"Status": "Failed", "Exception": str(e)}
	
	return json.dumps(resp)