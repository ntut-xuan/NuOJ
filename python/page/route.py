import asana_util as asana
import json
import pytz
import setting_util
from datetime import datetime
from dateutil import parser
from flask import Blueprint, request, render_template

page = Blueprint("page", __name__)

@page.route("/", methods=["GET"])
def returnIndex():
    SID = request.cookies.get("SID")
    return render_template("index.html", **locals())

@page.route("/dev_progress", methods=["GET"])
def progressPage():
    asana_util = asana.AsanatUil(json.loads(open("/etc/nuoj/setting.json", "r").read())["asana"]["token"])
    fetch_section_id = ["1202538198680473", "1202538198680519", "1202538198680522", "1202538198680525", "1202561659397276", "1202561659397287"]
    section_color = ["bg-orange-400", "bg-green-400", "bg-blue-400", "bg-purple-400", "bg-cyan-400", "bg-teal-400"]
    completed_task = asana_util.get_tasks("1202538198680466")
    task_count_by_section = {}
    complete_task_count_by_section = {}
    section_complete_percentage = {}
    section_task_info = {}
    completed_task_info = []

    for task in completed_task:
        task_section_gid = task["memberships"][0]["section"]["gid"]
        task_section_name = task["memberships"][0]["section"]["name"]
        if task_section_gid not in task_count_by_section:
            task_count_by_section[task_section_gid] = 0
            complete_task_count_by_section[task_section_gid] = 0
            section_task_info[task_section_gid] = []
        task_count_by_section[task_section_gid] += 1
        if task["completed"] and task_section_gid in fetch_section_id:
            index = fetch_section_id.index(task_section_gid)
            card_background_color = section_color[index]
            completed_time = parser.parse(task["completed_at"]).astimezone(pytz.timezone("Asia/Taipei"))
            completed_time_string = datetime.strftime(completed_time, "%Y-%m-%d %H:%M:%S")
            assignee_photo = None
            if task["assignee"]["photo"] == None:
                assignee_photo = "/static/logo_min.png"
            else:
                assignee_photo = task["assignee"]["photo"]["image_128x128"]
            completed_task_info.append({
                "task_section_name": task_section_name, "task_name": task["name"], 
                "task_complete_time": completed_time_string, "task_assignee": task["assignee"]["name"], 
                "task_assignee_photo": assignee_photo, "task_color": card_background_color})
            complete_task_count_by_section[task_section_gid] += 1
        section_complete_percentage[task_section_gid] = complete_task_count_by_section[task_section_gid] / task_count_by_section[task_section_gid]

    completed_task_info = sorted(completed_task_info, key=lambda d : d["task_complete_time"], reverse=True)
    frontend_pc = int(section_complete_percentage["1202538198680473"] * 100)
    backend_pc = int(section_complete_percentage["1202538198680519"] * 100)
    judge_pc = int(section_complete_percentage["1202538198680522"] * 100)
    other_pc = int(section_complete_percentage["1202538198680525"] * 100)
    database_pc = int(section_complete_percentage["1202561659397276"] * 100)
    test_pc = int(section_complete_percentage["1202561659397287"] * 100)
    complete_pc = (frontend_pc + backend_pc + judge_pc + other_pc + database_pc) // 5
    
    return render_template("progress.html", **locals())

@page.route("/about", methods=["GET"])
def getAboutIndex():
    return render_template("about_us.html", **locals())

@page.route("/debug", methods=["GET"])
def getDebugPage():
    return render_template("debug.html", **locals())

@page.route("/status", methods=["GET"])
def getStatusPage():
    def status_to_plain_text(status: int) -> str:
        return "工作中" if status == 200 else "連接失敗"
    def status_to_color(status: int) -> str:
        return "bg-green-500" if status == 200 else "bg-red-500"
    def data_proc(data: dict) -> dict:
        return {
            "name": data["name"], 
            "status": status_to_plain_text(data["status"]), 
            "status_color": status_to_color(data["status"])
        } 
    web_app_heartbeat_info = [data_proc(data) for data in setting_util.web_app_heartbeat_check()]
    database_heartbeat_info = [data_proc(data) for data in setting_util.database_heartbeat_check()]
    judge_server_heartbeat_info = [data_proc(data) for data in setting_util.judge_server_heartbeat_check()]
    return render_template("status.html", **locals())