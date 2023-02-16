from dataclasses import dataclass
from uuid import uuid4

from api.auth.auth_util import _init_user_data_to_database, _init_profile_storage_file
from models import User

@dataclass
class OAuthLoginResult:
    email: str
    passed: bool

def _init_oauth_user_data_and_profile_if_user_not_exists(email: str):
    if not _is_user_exists(email):
        user_uid: str = str(uuid4())
        password: str = str(uuid4())
        _init_user_data_to_database(user_uid, password, None, email, email_verified=1)
        _init_profile_storage_file(user_uid, email, email)
        
def _is_user_exists(email: str):
    user: User | None = User.query.filter(User.email == email).first()
    
    return user is not None