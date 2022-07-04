from flask import Flask, request, Response
from sandbox_enum import CodeType, Language
import isolate
import json
import traceback

app = Flask(__name__)

def init(code, language, type, box_id, option=None):
    isolate.init_sandbox(box_id)
    path, status = isolate.touch_text_file(code, type, language, box_id)
    return (path, status)

def finish(box_id):
    isolate.cleanup_sandbox(box_id)

def meta_data_to_dict(meta):
    meta_data = {}
    for data in meta.split("\n"):
        if(":" not in data):
            continue
        meta_data[data.split(":")[0]] = data.split(":")[1]
    return meta_data

def compile(language, type, box_id, option=None):
    try:
        meta = isolate.compile(type, language, box_id)
        meta_data = meta_data_to_dict(meta)

        if "status" in meta_data:
            meta_data["compile-result"] = "Failed"
        else:
            meta_data["compile-result"] = "OK"       
        
        return meta_data
    except Exception as e:
        print(traceback.format_exc())
        return (str(traceback.format_exc()), False)

def execute(language, type, testcase, box_id, option=None):
    try:
        output_data = []
        result_data = {}
        meta_data = compile(language, type, box_id)
        for i in range(len(testcase)):
            isolate.touch_text_file_by_file_name(testcase[i], "%d.in" % (i+1), 0)
        if(meta_data["compile-result"] == "Failed"):
            result_data["compile"] = meta_data
            return result_data
        output = isolate.execute(type, len(testcase), box_id)
        for data in output:
            data_dict = {}
            data_dict["meta"] = meta_data_to_dict(data[0])
            data_dict["output"] = data[1]
            output_data.append(data_dict)
        result_data["compile"] = meta_data
        result_data["execute"] = output_data
        return result_data
    except Exception as e:
        print(traceback.format_exc())
        return (str(traceback.format_exc()), False)

def judge(language, testcase, box_id, option=None):
    try:
        result = {}
        # 編譯 checker
        result["checker-compile"]  = compile(language, CodeType.CHECKER.value, box_id)
        if(result["checker-compile"]["compile-result"] == "Failed"):
            return result
        # 運行 solution
        result["solution_execute"] = execute(language, CodeType.SOLUTION.value, testcase, box_id)
        if(result["solution_execute"]["compile"]["compile-result"] == "Failed"):
            return result
        # 運行 submit
        result["submit_execute"]   = execute(language, CodeType.SUBMIT.value, testcase, box_id)
        if(result["submit_execute"]["compile"]["compile-result"] == "Failed"):
            return result
        # 運行 judge
        judge_meta_list = isolate.checker(len(testcase), box_id)
        judge_meta_data = []
        for data in judge_meta_list:
            judge_meta_data.append(meta_data_to_dict(data))
        result["judge_result"] = judge_meta_data

        report = []
        for i in range(len(judge_meta_data)):
            report_dict = {"verdict": "", "time": result["submit_execute"]["execute"][i]["meta"]["time"]}
            report_dict["verdict"] =  "AC" if judge_meta_data[i]["exitcode"] == "0" else "WA"
            report.append(report_dict)

        result["report"] = report
        del result["judge_result"]
        del result["solution_execute"]["execute"]
        del result["submit_execute"]["execute"]

        return result
    except Exception as e:
        print(traceback.format_exc())
        return (str(traceback.format_exc()), False)

@app.route("/judge", methods=["POST"])
def judge_route():
    data = json.loads(request.data.decode("utf-8"))
    user_code = data["code"]
    test_case = data["testcase"]
    execution_type = data["execution"]
    result = {}
    status = None
    box_id = 0

    _, status = init(user_code, Language.CPP.value, CodeType.SUBMIT.value, box_id)
    
    if "solution" in data:
        solution_code = data["solution"]
        _, status = init(solution_code, Language.CPP.value, CodeType.SOLUTION.value, box_id)
    if "checker" in data:
        checker_code = data["checker"]
        _, status = init(checker_code, Language.CPP.value, CodeType.CHECKER.value, box_id)

    isolate.touch_text_file_by_file_name(open("./testlib.h", "r").read(), "testlib.h", box_id)

    if execution_type == "C":
        result = compile(Language.CPP.value, CodeType.SUBMIT.value, box_id)
    elif execution_type == "E":
        result = execute(Language.CPP.value, CodeType.SUBMIT.value, test_case, box_id)
    elif execution_type == "J":
        result = judge(Language.CPP.value, test_case, box_id)
    
    finish(box_id)

    response = {"status": "OK", "type": execution_type}
    if(status == False):
        response["status"] = "Failed"
        response["message"] = result
    else:
        response["data"] = result
    return Response(json.dumps(response), mimetype="application/json")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)