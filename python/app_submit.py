from flask import *
import database_util as database_util

submit = Blueprint('submit', __name__)

@submit.route("/submit/", methods=["POST"])
def submitProblem(problemID):
    '''
    提交程式碼的接口，使用 RestFul 風格撰寫。
        Require:
            需要 SID 資訊。
        Parameter:
            problemID: 要提交的題目 ID。
    '''
    data = request.data
    code = data["code"]
    