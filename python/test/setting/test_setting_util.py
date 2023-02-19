from typing import Any

import pytest
from flask import Flask

from setting.util import Setting, SettingBuilder, MailSetting


@pytest.fixture
def setting_dict() -> dict[str, Any]:
    setting_dict = {
        "oauth": {
            "github": {"enable": True, "client_id": "", "secret": ""},
            "google": {
                "enable": False,
                "client_id": "",
                "secret": "",
                "redirect_url": "",
            },
        },
        "asana": {"token": ""},
        "mail": {
            "enable": True,
            "server": "fake-smtp-server",
            "port": "1025",
            "mailname": "test@nuoj.com",
            "password": "nuoj_test",
            "redirect_url": "http://nuoj.ntut-xuan.net/verify_mail",
        },
    }
    return setting_dict


def test_setting_builder_from_dict_should_return_valid_setting_object(
    setting_dict: dict[str, Any]
):
    setting: Setting = SettingBuilder().from_dict(setting_dict)

    assert setting.asana.__dict__ == setting_dict["asana"]
    assert setting.mail.__dict__ == setting_dict["mail"]
    assert setting.oauth.github.__dict__ == setting_dict["oauth"]["github"]
    assert setting.oauth.google.__dict__ == setting_dict["oauth"]["google"]


def test_edit_setting_with_assign_value_should_replace_the_setting_value(
    setting_dict: dict[str, Any]
):
    setting: Setting = SettingBuilder().from_dict(setting_dict)

    setting.oauth.github.enable = False

    assert setting.oauth.github.enable == False
