from dataclasses import dataclass

@dataclass
class OAuthLoginResult:
    email: str
    passed: bool
    token: str