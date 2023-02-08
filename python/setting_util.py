import json
import platform
import requests
import database_util

setting = json.loads(open("/etc/nuoj/setting.json", "r").read())

def github_oauth_enable() -> bool:
    '''
    回傳使用者是否開啟 Github OAuth 功能
    '''
    return setting["oauth"]["github"]["enable"]

def github_oauth_client_id() -> str:
    '''
    回傳使用者 Github OAuth 的 client ID
    '''
    return setting["oauth"]["github"]["client_id"]

def github_oauth_secret() -> str:
    '''
    回傳使用者 Github OAuth 的 secret
    '''
    return setting["oauth"]["github"]["secret"]

def google_oauth_enable() -> bool:
    '''
    回傳使用者是否開啟 Google OAuth 功能
    '''
    return setting["oauth"]["google"]["enable"]

def google_oauth_client_id() -> str:
    '''
    回傳使用者 Google OAuth 的 client ID
    '''
    return setting["oauth"]["google"]["client_id"]

def google_oauth_redirect_url() -> str:
    '''
    回傳使用者 Google OAuth 的 client ID
    '''
    return setting["oauth"]["google"]["redirect_url"]

def mail_verification_enable() -> bool:
    '''
    回傳使用者是否開啟信箱驗證功能
    '''
    return setting["mail"]["enable"]

def mail_info() -> str:
    return setting["mail"]["info"]

def mail_redirect_url() -> str:
    '''
    回傳信箱 redirect_url 設置值
    '''
    return setting["mail"]["redirect_url"]

def database_info() -> list:
    '''
    回傳使用者設定的 database 連結序列
    '''
    return setting["architecture"]["database"]

def master_database_url() -> str:
    '''
    回傳使用者設定的 master database 連結
    '''
    for data in database_info():
        if data["type"] == "master":
            return data["url"] + ":" + data["port"]
    return None

def slave_database_url() -> str:
    '''
    回傳使用者設定的 slave database 連結，以序列表示
    '''
    slave_database = []
    for data in database_info():
        if data["type"] == "slave":
            slave_database.append(data["url"] + ":" + data["port"])
    return slave_database

def master_database_token() -> str:
    '''
    回傳使用者設定的 master database 的 token
    '''
    for data in database_info():
        if data["type"] == "master":
            return data["token"]
    return None

def web_app_info() -> list:
    '''
    回傳使用者設定的 web application 資料序列
    '''
    return setting["architecture"]["web_app"]

def judge_server_info() -> list:
    '''
    回傳使用者設定的 judge server 資料序列
    '''
    return setting["architecture"]["judge_server"]

def web_app_heartbeat_check() -> list:
    '''
    回傳 web application 資料序列的心跳，以序列呈現
    '''
    status_list = []
    for data in web_app_info():
        try:
            req = requests.get(data["url"] + ":" + data["port"] + "/heartbeat")
            status_list.append({"name": data["name"], "status": req.status_code})
        except requests.exceptions.ConnectionError as e:
            status_list.append({"name": data["name"], "status": 502})
    return status_list

def database_heartbeat_check() -> list:
    '''
    回傳 database 資料序列的心跳，以序列呈現
    '''
    status_list = []
    for data in database_info():
        try:
            database_util.connect_database()
            status_list.append({"name": data["name"], "status": 200})
        except requests.exceptions.ConnectionError as e:
            status_list.append({"name": data["name"], "status": 502})
    return status_list

def judge_server_heartbeat_check() -> list:
    '''
    回傳 judge server 資料序列的心跳，以序列呈現
    '''
    status_list = []
    for data in judge_server_info():
        try:
            req = requests.get(data["url"] + ":" + data["port"] + "/heartbeat")
            status_list.append({"name": data["name"], "status": req.status_code})
        except requests.exceptions.ConnectionError as e:
            status_list.append({"name": data["name"], "status": 502})
    return status_list

def cpu_name() -> str:
    '''
    回傳使用者目前架設的 CPU 名稱
    '''
    return platform.processor()
