#!/usr/bin/env python3
import pymysql
import os
import subprocess
import json
from threading import Timer
from loguru import logger

def connect_mysql():
    
    # connect NuOJ Database
    db_setting = {
        "host": "localhost",
        "port": 3306,
        "user": "NuOJJudger",
        "password": "Nu0JJ!@#$",
        "db": "NuOJ",
        "charset": "utf8"
    }
    conn = None
    try:
        conn = pymysql.connect(**db_setting)
    except Exception as ex:
        print(ex)
    finally:
        return conn

def judge(conn):
    #try:

    ID = ""
    language = ""
    problemID = ""

    # Check if it's necessary to judge
    with conn.cursor() as cursor:
        cursor.execute("select COUNT(*) from `submission` where VerdictResult='Pending';")
        fetchResult = cursor.fetchone()
        if(int(fetchResult[0]) == 0):
            return
        cursor.close()
    

    # Check judge target ID, target language and target prooblemID.
    with conn.cursor() as cursor:
        cursor.execute("select * from `submission` where VerdictResult='Pending';")
        fetchResult = cursor.fetchone()
        ID = str(fetchResult[0])
        language = fetchResult[3]
        problemID = fetchResult[4]
        cursor.close()

    logger.info("Judge Submission " + str(ID))

    # init isolate
    subprocess.call("isolate --init", shell=True)

    # Move data
    subprocess.call(("cp /opt/nuoj/submit_code/submission_%d.cpp /var/local/lib/isolate/0/box" % int(ID)), shell=True)

    # Move testdata
    subprocess.call(("cp /opt/nuoj/problem_testcase/%s/* /var/local/lib/isolate/0/box" % problemID), shell=True)

    # Check testdata count
    file = open("/opt/nuoj/problem_testcase/%s/%s.json" % (problemID, problemID))
    data = json.load(file)
    testcase_count = int(data["testcaseCount"])

    # Execute isolate -- compile
    logger.debug("isolate -- compile: submission_%d" % (int(ID)))
    subprocess.call("touch /opt/nuoj/metafile_storage/submission_%d_compile.m" % (int(ID)), shell=True)
    subprocess.call("chmod 777 /opt/nuoj/metafile_storage/submission_%d_compile.m" % (int(ID)), shell=True)
    #logger.debug(result.stdout.decode("utf-8").replace('\n',''))
    subprocess.call("isolate --time=2 -p --full-env --meta=\"/opt/nuoj/metafile_storage/submission_%d_compile.m\" --run -- /usr/bin/g++ submission_%d.cpp -o submission_%d.o" % (int(ID), int(ID), int(ID)), shell=True)
    subprocess.call("isolate --run -- /usr/bin/chmod 777 submission_%d.o" % (int(ID)), shell=True)

    # Execute isolate -- run testcase
    for i in range(1, testcase_count+1):
        logger.debug("isolate -- run_testcase: submission_%d" % (int(i)))
        subprocess.call("isolate --run -- /usr/bin/touch %d.out" % (int(i)), shell=True)
        subprocess.call("touch /opt/nuoj/metafile_storage/submission_%d_%d_execute.m" % (int(ID), int(i)), shell=True)
        subprocess.call("chmod 777 /opt/nuoj/metafile_storage/submission_%d_%d_execute.m" % (int(ID), int(i)), shell=True)
        logger.info("isolate --time=2 -p --full-env --stdin=\"%d.in\" --stdout=\"%d.out\" --meta=\"/opt/nuoj/metafile_storage/submission_%d_%d_execute.m\" --run submission_%d.o" % (int(i), int(i), int(ID), int(i), int(ID)))
        subprocess.call("isolate --wall-time=2 -p --full-env --stdin=\"%d.in\" --stdout=\"%d.out\" --meta=\"/opt/nuoj/metafile_storage/submission_%d_%d_execute.m\" --run submission_%d.o" % (int(i), int(i), int(ID), int(i), int(ID)), shell=True)

    # check result and generate result file
    judgeResult = {}
    judgeResult_status = "AC"
    judgeResult_time = 0
    for i in range(1, testcase_count+1):
        metafile_map = {}
        file = open("/opt/nuoj/metafile_storage/submission_%d_%d_execute.m" % (int(ID), int(i)), "r")
        split = file.read().split("\n")
        status = ""
        time = 0
        metafile_data = {} 
        for a in split:
            print(a)
            if(a == ""):
                continue
            b = a.split(":")
            metafile_data[b[0]] = b[1]


        if "status" in metafile_data.keys():
            status = metafile_data["status"]
            message = metafile_data["message"]
            if (status == "RE"):
                time = metafile_data["time-wall"]
                judgeResult[i] = [status, time, message]
            elif (status == "TO"):
                time = metafile_data["time-wall"]
                judgeResult[i] = [status, time, message]
            elif (status == "XX"):
                judgeResult[i] = ["CE", time, message]

        if(status == ""):

            time = metafile_data["time-wall"]

            out_file = open("/var/local/lib/isolate/0/box/%d.out" % (i), "r")
            ans_file = open("/var/local/lib/isolate/0/box/%d.ans" % (i), "r")

            out_file_text = out_file.read().split("\n")
            ans_file_text = ans_file.read().split("\n")

            if(len(out_file_text) != len(ans_file_text)):
                judgeResult[i] = ["OLE", time, "except count of output-line doesn't equals count of answer-line."]

            wrong_answer_flag = False

            for i in range(len(out_file_text)):
                out_file_line = out_file_text[i].strip()
                ans_file_line = ans_file_text[i].strip()
                if (out_file_line != ans_file_line):
                    wrong_answer_flag = True
                    judgeResult[i] = ["WA", time, "Except " + ans_file_line + ", but output " + a]
                    break
            
            if(wrong_answer_flag == False):
                judgeResult[i] = ["AC", time, "OK."]
                status = "OK"

            out_file.close()
            ans_file.close()
        
        judgeResult_time = max(judgeResult_time, float(judgeResult[i][1]))
        if(judgeResult[i][0] != "AC"):
            judgeResult_status = judgeResult[i][0]
            

    judgeResult["status"] = judgeResult_status
    judgeResult["time"] = judgeResult_time
    json_data = json.dumps(judgeResult)
    result_file = open("/opt/nuoj/submission_result/submission_%d.nr" % (int(ID)), "w", encoding="utf-8")
    result_file.write(json_data.encode("utf-8").decode("utf-8"))
    result_file.close()

    # commit into database
    with conn.cursor() as cursor:
        command = "UPDATE `submission` SET VerdictResult='%s', VerdictTime='%s', VerdictMemory='Unknown' WHERE submissionID=%s;" % (judgeResult["status"], str(judgeResult["time"]), str(ID))
        logger.debug(command)
        cursor.execute(command)
        conn.commit()
        cursor.close()

    # clean container
    subprocess.call("isolate --cleanup", shell=True)
    #except Exception as ex:
    #    print(ex)

while True:
    conn = connect_mysql()
    judge(conn)