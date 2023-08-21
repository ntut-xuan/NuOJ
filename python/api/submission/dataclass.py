from enum import Enum
from dataclasses import dataclass
from typing import Any


class JudgeStatus(Enum):
    AC = "AC"
    WA = "WA"
    TLE = "TLE"
    
class ResponseStatus(Enum):
    OK = "OK"


@dataclass
class JudgeMeta:
    time: float
    memory: int
    exitcode: int | None = None
    
    def __post_init__(self):
        self.memory = int(self.memory)
        self.time = float(self.time)
        if self.exitcode != None:
            self.exitcode = int(self.exitcode)


@dataclass
class JudgeCompileDetail:
    solution: JudgeMeta
    checker: JudgeMeta
    submit: JudgeMeta

    def __post_init__(self):
        self.checker = JudgeMeta(**self.checker)
        self.submit = JudgeMeta(**self.submit)
        self.solution = JudgeMeta(**self.solution)


@dataclass
class JudgeOutputSet:
    submit: str
    answer: str


@dataclass
class JudgeRuntimeInfo:
    checker: JudgeMeta | None = None
    submit: JudgeMeta | None = None
    solution: JudgeMeta | None = None

    def __post_init__(self):
        if self.checker is not None:
            self.checker = JudgeMeta(**self.checker)
        if self.submit is not None:
            self.submit = JudgeMeta(**self.submit)
        if self.solution is not None:
            self.solution = JudgeMeta(**self.solution)


@dataclass
class JudgeDetail:
    verdict: str
    output_set: JudgeOutputSet
    runtime_info: JudgeRuntimeInfo
    log: str

    def __post_init__(self):
        self.verdict = JudgeStatus(self.verdict).value
        self.output_set = JudgeOutputSet(**self.output_set)
        self.runtime_info = JudgeRuntimeInfo(**self.runtime_info)


@dataclass
class JudgeData:
    status: str
    message: str
    compile_detail: JudgeCompileDetail
    judge_detail: list[JudgeDetail]
    
    def __post_init__(self):
        self.status = JudgeStatus(self.status).value
        self.compile_detail = JudgeCompileDetail(**self.compile_detail)
        self.judge_detail = [JudgeDetail(**obj) for obj in self.judge_detail]


@dataclass
class JudgeResult:
    status: ResponseStatus
    data: JudgeData

    def __post_init__(self):
        self.status = ResponseStatus(self.status)
        self.data = JudgeData(**self.data)
