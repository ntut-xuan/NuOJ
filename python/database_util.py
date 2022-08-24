import json
import requests
import setting_util
import pymysql
import os
from tunnel_code import TunnelCode
from enum import Enum

def connect_database() -> pymysql.Connection:
    conn = pymysql.connect(host="127.0.0.1", user="NuOJService", password="Nu0JS!@#$", database="NuOJ")
    return conn

def command_execute(command: str, param: tuple) -> dict:
    '''
    這個函數可以讓你使用 MySQL 的指令，並將回傳結果轉成一個 dict 回傳。
        param:
            command: MySQL 的指令，需要可以正常運作。
            param: 參數化的參數。
        return:
            一個包含結果的 dict。
    '''
    conn = connect_database()
    with conn.cursor() as cursor:
        cursor.execute(command, param)
        conn.commit()
        if cursor.description != None:
            field_name = [name[0] for name in cursor.description]
            result = cursor.fetchall()
            result_list = []
            for data in result:
                result_list.append(dict(zip(field_name, list(data))))
            return result_list
        else:
            return {}

def file_storage_tunnel_exist(filename: str, tunnel: TunnelCode) -> bool:
    path = "/etc/nuoj/storage/%s/%s" % (tunnel.value, filename)
    return os.path.exists(path)

def file_storage_tunnel_read(filename: str, tunnel: TunnelCode) -> str:
    path = "/etc/nuoj/storage/%s/%s" % (tunnel.value, filename)
    if file_storage_tunnel_exist(filename, tunnel):
        with open(path, "r") as file:
            return file.read()
    else:
        return ""
    
def byte_storage_tunnel_read(filename: str, tunnel: TunnelCode) -> bytes:
    path = "/etc/nuoj/storage/%s/%s" % (tunnel.value, filename)
    if file_storage_tunnel_exist(filename, tunnel):
        with open(path, "rb") as file:
            return file.read()
    else:
        return 0

def file_storage_tunnel_write(filename: str, data : str, tunnel: TunnelCode) -> None:
    path = "/etc/nuoj/storage/%s/%s" % (tunnel.value, filename)
    with open(path, "w") as file:
        file.write(data)
        file.close()

def byte_storage_tunnel_write(filename: str, data: bytes, tunnel: TunnelCode) -> None:
    path = "/etc/nuoj/storage/%s/%s" % (tunnel.value, filename)
    with open(path, "wb") as file:
        file.write(data)
        file.close()


def file_storage_tunnel_del(filename: str, tunnel: TunnelCode) -> str:
    path = "/etc/nuoj/storage/%s/%s" % (tunnel.value, filename)
    if file_storage_tunnel_exist(filename, tunnel):
        os.remove(path)
    else:
        return ""