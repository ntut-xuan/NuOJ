import os
from datetime import timedelta
from urllib.parse import quote

SECRET_KEY: bytes = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=31)
STORAGE_PATH: str = "/etc/nuoj/storage"
SETTING_FILE_PATH: str = "/etc/nuoj/setting.json"
SQLALCHEMY_DATABASE_URI: str = (
    "mysql+pymysql://nuoja:{password}@mariadb:3306/nuoj".format(
        password=quote("@nuoja2023")
    )
)
