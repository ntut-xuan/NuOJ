from enum import Enum

class CodeType(Enum):
    SUBMIT = "submit_code"
    SOLUTION = "solution"
    VALIDATE = "validate"
    CHECKER = "checker"
    META = "meta"


class Language(Enum):
    CPP = ".cpp"
    PYTHON = ".py"
    NONE = ""