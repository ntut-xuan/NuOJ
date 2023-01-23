import os
from datetime import timedelta

SECRET_KEY: str = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=31)
