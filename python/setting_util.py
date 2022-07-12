import json

setting = json.loads(open("/opt/nuoj/setting.json", "r").read())

def github_oauth_enable() -> bool:
    '''
    回傳使用者是否開啟 Github OAuth 功能
    '''
    return setting["oauth"]["github"]["enable"]

def google_oauth_enable() -> bool:
    '''
    回傳使用者是否開啟 Google OAuth 功能
    '''
    return setting["oauth"]["google"]["enable"]

def mail_verification_enable() -> bool:
    '''
    回傳使用者是否開啟信箱驗證功能
    '''
    return setting["mail"]["enable"]

def master_database_url() -> str:
    '''
    回傳使用者設定的 master database 連結
    '''
    return setting["database-master"]["url"] + ":" + setting["database-master"]["port"]

def master_database_token() -> str:
    '''
    回傳使用者設定的 master database 的 token
    '''
    return setting["database-master"]["token"]
