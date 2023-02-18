import json
import requests
# import setting_util
import pymysql
import os
from tunnel_code import TunnelCode
from enum import Enum
from typing import Any

from flask import current_app


# def connect_database() -> pymysql.Connection:
#     conn = pymysql.connect(
#         host="mariadb", user="nuoja", password="@nuoja2023", database="nuoj"
#     )
#     return conn


# def command_execute(command: str, param: tuple) -> list[dict[str, Any]]:
#     """
#     這個函數可以讓你使用 MySQL 的指令，並將回傳結果轉成一個 dict 回傳。
#         param:
#             command: MySQL 的指令，需要可以正常運作。
#             param: 參數化的參數。
#         return:
#             一個包含結果的 dict。
#     """
#     conn = connect_database()
#     with conn.cursor() as cursor:
#         cursor.execute(command, param)
#         conn.commit()
#         if cursor.description != None:
#             field_name = [name[0] for name in cursor.description]
#             result = cursor.fetchall()
#             result_list = []
#             for data in result:
#                 result_list.append(dict(zip(field_name, list(data))))
#             return result_list
#         else:
#             return [{}]


def file_storage_tunnel_exist(filename: str, tunnel: TunnelCode) -> bool:
    file_path = _make_file_path(tunnel, filename)
    return os.path.exists(file_path)


def file_storage_tunnel_read(filename: str, tunnel: TunnelCode) -> str:
    file_path = _make_file_path(tunnel, filename)
    if file_storage_tunnel_exist(filename, tunnel):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return ""


def byte_storage_tunnel_read(filename: str, tunnel: TunnelCode) -> bytes:
    file_path = _make_file_path(tunnel, filename)
    if file_storage_tunnel_exist(filename, tunnel):
        with open(file_path, "rb") as file:
            return file.read()
    else:
        return b''


def file_storage_tunnel_write(filename: str, data: str, tunnel: TunnelCode) -> None:
    file_path = _make_file_path(tunnel, filename)
    with open(file_path, "w") as file:
        file.write(data)
        file.close()


def byte_storage_tunnel_write(filename: str, data: bytes, tunnel: TunnelCode) -> None:
    file_path = _make_file_path(tunnel, filename)
    with open(file_path, "wb") as file:
        file.write(data)
        file.close()


def file_storage_tunnel_del(filename: str, tunnel: TunnelCode) -> None:
    file_path = _make_file_path(tunnel, filename)
    if file_storage_tunnel_exist(filename, tunnel):
        os.remove(file_path)


def _make_file_path(tunnel: TunnelCode, filename: str) -> str:
    storage_path = current_app.config.get("STORAGE_PATH")
    assert storage_path is not None
    file_path = "%s/%s/%s" % (storage_path, tunnel.value, filename)
    return file_path
