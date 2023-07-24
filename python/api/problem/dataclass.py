from dataclasses import dataclass

from models import User


@dataclass
class ProblemHead:
    title: str
    problem_pid: int
    time_limit: float
    memory_limit: float

    def __dict__(self):
        return {
            "title": self.title,
            "problem_pid": self.problem_pid,
            "time_limit": self.time_limit,
            "memory_limit": self.memory_limit
        }


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

    def __dict__(self):
        return {
            "head": self.head.__dict__(),
            "content": self.content.__dict__(),
            "author": {
                "user_uid": self.author.user_uid, 
                "handle": self.author.handle
            },
        }