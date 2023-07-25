from dataclasses import dataclass
from typing import Any

from models import User

@dataclass
class ProblemHeadWithoutPid:
    title: str
    time_limit: float
    memory_limit: float

    def __dict__(self):
        return {
            "title": self.title,
            "time_limit": self.time_limit,
            "memory_limit": self.memory_limit
        }


@dataclass
class ProblemHead(ProblemHeadWithoutPid):
    problem_pid: int

    def __dict__(self):
        problem_head: dict[str, Any] = super().__dict__()
        problem_head |= {"problem_pid": self.problem_pid}
        return problem_head


@dataclass
class ProblemContent:
    description: str
    input_description: str
    output_description: str
    note: str

    def __dict__(self):
        return {
            "description": self.description,
            "input_description": self.input_description,
            "output_description": self.output_description,
            "note": self.note
        }


@dataclass
class ProblemData:
    head: ProblemHead
    content: ProblemContent
    author: User

    def __storage_dict__(self):
        head: dict[str, Any] = self.head.__dict__()
        content: dict[str, Any] = self.content.__dict__()
        del head["problem_pid"]
        return {
            "head": head,
            "content": content
        }

    def __dict__(self):
        return {
            "head": self.head.__dict__(),
            "content": self.content.__dict__(),
            "author": {
                "user_uid": self.author.user_uid, 
                "handle": self.author.handle
            },
        }