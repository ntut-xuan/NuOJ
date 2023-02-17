import database_util
import json
import platform
import requests
from pathlib import Path
from typing import Any
from functools import wraps


class Setting:
    def __init__(self):
        self.setting = None

    def from_dict(self, dict: dict[str, Any]):
        self.setting = dict
        return self

    def from_json_file(self, path: Path):
        with open(path, "r") as file:
            plain_setting_json: str = file.read()
            self.setting = json.loads(plain_setting_json)
            return self

    def github_oauth_enable(self) -> bool:
        """
        回傳使用者是否開啟 Github OAuth 功能
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["oauth"]["github"]["enable"]

    def github_oauth_client_id(self) -> str:
        """
        回傳使用者 Github OAuth 的 client ID
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["oauth"]["github"]["client_id"]

    def github_oauth_secret(self) -> str:
        """
        回傳使用者 Github OAuth 的 client ID
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["oauth"]["github"]["secret"]

    def google_oauth_enable(self) -> bool:
        """
        回傳使用者是否開啟 Google OAuth 功能
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["oauth"]["google"]["enable"]

    def google_oauth_client_id(self) -> str:
        """
        回傳使用者 Google OAuth 的 client ID
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["oauth"]["google"]["client_id"]

    def google_oauth_redirect_url(self) -> str:
        """
        回傳使用者 Google OAuth 的 client ID
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["oauth"]["google"]["redirect_url"]

    def google_oauth_secret(self) -> str:
        """
        回傳使用者 Google OAuth 的 client ID
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["oauth"]["google"]["secret"]

    def mail_verification_enable(self) -> bool:
        """
        回傳使用者是否開啟信箱驗證功能
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["mail"]["enable"]

    def mail_server(self) -> str:
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["mail"]["server"]

    def mail_port(self) -> int:
        self._raise_value_error_if_setting_is_not_setup()
        return int(self.setting["mail"]["port"])

    def mail_mailname(self) -> str:
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["mail"]["mailname"]

    def mail_password(self) -> str:
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["mail"]["password"]

    def mail_info(self) -> str:
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["mail"]["info"]

    def mail_redirect_url(self) -> str:
        """
        回傳信箱 redirect_url 設置值
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["mail"]["redirect_url"]

    def database_info(self) -> list:
        """
        回傳使用者設定的 database 連結序列
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["architecture"]["database"]

    def master_database_url(self) -> str | None:
        """
        回傳使用者設定的 master database 連結
        """
        for data in self.database_info():
            if data["type"] == "master":
                return data["url"] + ":" + data["port"]
        return None

    def slave_database_url(self) -> list[str]:
        """
        回傳使用者設定的 slave database 連結，以序列表示
        """
        slave_database = []
        for data in self.database_info():
            if data["type"] == "slave":
                slave_database.append(data["url"] + ":" + data["port"])
        return slave_database

    def master_database_token(self) -> str | None:
        """
        回傳使用者設定的 master database 的 token
        """
        for data in self.database_info():
            if data["type"] == "master":
                return data["token"]
        return None

    def web_app_info(self) -> list:
        """
        回傳使用者設定的 web application 資料序列
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["architecture"]["web_app"]

    def judge_server_info(self) -> list:
        """
        回傳使用者設定的 judge server 資料序列
        """
        self._raise_value_error_if_setting_is_not_setup()
        return self.setting["architecture"]["judge_server"]

    # def web_app_heartbeat_check(self) -> list:
    #     """
    #     回傳 web application 資料序列的心跳，以序列呈現
    #     """
    #     status_list = []
    #     for data in self.web_app_info():
    #         try:
    #             req = requests.get(data["url"] + ":" + data["port"] + "/heartbeat")
    #             status_list.append({"name": data["name"], "status": req.status_code})
    #         except requests.exceptions.ConnectionError as e:
    #             status_list.append({"name": data["name"], "status": 502})
    #     return status_list

    # def database_heartbeat_check(self) -> list:
    #     """
    #     回傳 database 資料序列的心跳，以序列呈現
    #     """
    #     status_list = []
    #     for data in self.database_info():
    #         try:
    #             database_util.connect_database()
    #             status_list.append({"name": data["name"], "status": 200})
    #         except requests.exceptions.ConnectionError as e:
    #             status_list.append({"name": data["name"], "status": 502})
    #     return status_list

    # def judge_server_heartbeat_check(self) -> list:
    #     """
    #     回傳 judge server 資料序列的心跳，以序列呈現
    #     """
    #     status_list = []
    #     for data in self.judge_server_info():
    #         try:
    #             req = requests.get(data["url"] + ":" + data["port"] + "/heartbeat")
    #             status_list.append({"name": data["name"], "status": req.status_code})
    #         except requests.exceptions.ConnectionError as e:
    #             status_list.append({"name": data["name"], "status": 502})
    #     return status_list

    def cpu_name(self) -> str:
        """
        回傳使用者目前架設的 CPU 名稱
        """
        return platform.processor()

    def _raise_value_error_if_setting_is_not_setup(self):
        if self.setting is None:
            raise ValueError("Setting is not setup yet!")