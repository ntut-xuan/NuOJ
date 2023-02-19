import json
from pathlib import Path
from typing import Any
from dataclasses import dataclass


@dataclass
class OAuthSettingObject:
    enable: bool
    client_id: str
    secret: str


@dataclass
class GithubSetting(OAuthSettingObject):
    pass


@dataclass
class GoogleSetting(OAuthSettingObject):
    redirect_url: str


@dataclass
class OAuthSetting:
    github: GithubSetting
    google: GoogleSetting


@dataclass
class AsanaSetting:
    token: str


@dataclass
class MailSetting:
    enable: bool
    server: str
    port: int
    mailname: str
    password: str
    redirect_url: str


@dataclass
class Setting:
    oauth: OAuthSetting
    mail: MailSetting
    asana: AsanaSetting | None = None


class SettingBuilder:
    def __init__(self) -> None:
        self.setting: Setting | None = None

    def from_dict(self, dict: dict[str, Any]) -> Setting:
        self.setting = Setting(
            oauth=OAuthSetting(
                github=GithubSetting(**dict["oauth"]["github"]),
                google=GoogleSetting(**dict["oauth"]["google"]),
            ),
            mail=MailSetting(**dict["mail"]),
            asana=AsanaSetting(**dict["asana"]),
        )
        return self.setting

    def from_json_file(self, path: Path) -> Setting:
        with open(path, "r") as file:
            plain_setting_json: str = file.read()
            setting_dict: dict[str, Any] = json.loads(plain_setting_json)
            self.setting = self.from_dict(setting_dict)
            return self.setting
