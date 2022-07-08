import redis
import json
import requests

def connect_master_database():
    setting = json.loads(open("/opt/nuoj/setting.json", "r").read())
    data = setting["database-master"]
    url = data["url"] + ":" + data["port"]
    req = requests.get(url + "/heartbeat")
    if req.status_code == 200:
        return url
    return None

def connect_slave_database():
    setting = json.loads(open("/opt/nuoj/setting.json", "r").read())
    database_list = setting["database-slave"]
    if len(database_list) != 0:
        for data in database_list:
            url = data["url"] + ":" + data["port"]
            req = requests.get(url + "/heartbeat")
            if req.status_code == 200:
                return url
        return None
    else:
        return connect_master_database()

def get_data(sub_url, parameter, token=""):
    header = {"Content-Type": "application/json", "Accept": "*/*", "Authorizon": "Barear %s" % (token)}
    return json.loads(requests.get(connect_slave_database() + sub_url, params=parameter, headers=header).text)

def post_data(sub_url, parameter, data, token=""):
    header = {"Content-Type": "application/json", "Accept": "*/*", "Authorizon": "Barear %s" % (token)}
    return json.loads(requests.post(connect_master_database() + sub_url, params=parameter, headers=header, data=data).text)

def put_data(sub_url, parameter, data, token=""):
    header = {"Content-Type": "application/json", "Accept": "*/*", "Authorizon": "Barear %s" % (token)}
    return json.loads(requests.put(connect_master_database() + sub_url, params=parameter, headers=header, data=data).text)

def delete_data(sub_url, parameter, data, token=""):
    header = {"Content-Type": "application/json", "Accept": "*/*", "Authorizon": "Barear %s" % (token)}
    return json.loads(requests.delete(connect_master_database() + sub_url, params=parameter, headers=header, data=data).text)