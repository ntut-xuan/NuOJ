from flask import Flask, request, Response
from sandbox_enum import CodeType, Language
import isolate
import json

app = Flask(__name__)

def compile(code, language, type, box_id, option=None):
    try:
        # 初始化沙箱
        isolate.init_sandbox(box_id)

        # 將程式檔案創建至沙箱內
        path, status = isolate.touch_text_file(code, type, language, 0)
        if status == True:
            print("create file at", path)

        # 執行編譯
        meta, status = isolate.compile(type, language, 0)
        if status == True:
            print(meta)

        # 處理 meta file 並回傳
        meta_data = {}
        for data in meta.split("\n"):
            if(":" not in data):
                continue
            meta_data[data.split(":")[0]] = data.split(":")[1]
        if "status" in meta_data:
            meta_data["compile-result"] = "Failed"
        else:
            meta_data["compile-result"] = "OK"
        return (meta_data, status)
    except Exception as e:
        return (str(e), False)


@app.route("/judge", methods=["POST"])
def judge():
    user_code = json.loads(request.data.decode("utf-8"))["code"]
    compile_result, status = compile(user_code, Language.CPP.value, CodeType.SUBMIT.value, 0)
    response = {"status": "OK"}
    if(status == False):
        response["status"] = "Failed"
        response["message"] = compile_result
    else:
        response["meta"] = compile_result
    return Response(json.dumps(response), mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)