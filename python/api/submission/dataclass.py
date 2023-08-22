from enum import Enum
from dataclasses import dataclass, field
from typing import Any


class JudgeStatus(Enum):
    AC = "AC"
    CE = "CE"
    CCE = "CCE"
    CMLE = "CMLE"
    CRE = "CRE"
    CTLE = "CTLE"
    WA = "WA"
    RE = "RE"
    TLE = "TLE"
    MLE = "MLE"
    SMLE = "SMLE"
    STLE = "STLE"
    SRE = "SRE"
    
class ResponseStatus(Enum):
    OK = "OK"


@dataclass
class JudgeMeta:
    time: float
    memory: int
    exitcode: int | None = None
    exitsig: int | None = None
    
    def __post_init__(self):
        self.memory = int(self.memory)
        self.time = float(self.time)
        if self.exitcode != None:
            self.exitcode = int(self.exitcode)
        if self.exitsig != None:
            self.exitsig = int(self.exitsig)


@dataclass
class JudgeCompileDetail:
    solution: JudgeMeta | None = None
    checker: JudgeMeta | None = None
    submit: JudgeMeta | None = None

    def __post_init__(self):
        if self.checker != None:
            self.checker = JudgeMeta(**self.checker)
        if self.submit != None:
            self.submit = JudgeMeta(**self.submit)
        if self.solution != None:
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
    judge_detail: list[JudgeDetail] | None = None
    
    def __post_init__(self):
        self.status = JudgeStatus(self.status).value
        self.compile_detail = JudgeCompileDetail(**self.compile_detail)
        if self.judge_detail is not None:
            self.judge_detail = [JudgeDetail(**obj) for obj in self.judge_detail]
        else:
            self.judge_detail = []


@dataclass
class JudgeResult:
    status: ResponseStatus
    data: JudgeData

    def __post_init__(self):
        self.status = ResponseStatus(self.status)
        self.data = JudgeData(**self.data)
