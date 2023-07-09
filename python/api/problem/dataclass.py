from dataclasses import dataclass

from models import User


@dataclass
class ProblemHead:
    title: str
    problem_pid: int
    time_limit: float
    memory_limit: float


@dataclass
class ProblemContent:
    description: str
    input_description: str
    output_description: str
    note: str


@dataclass
class ProblemData:
    head: ProblemHead
    content: ProblemContent
    author: User

    def __dict__(self):
        return {
            "head": {
                "title": self.head.title,
                "time_limit": self.head.time_limit,
                "memory_limit": self.head.memory_limit,
                "problem_pid": self.head.problem_pid
            },
            "content": {
                "description": self.content.description,
                "input_description": self.content.input_description,
                "output_description": self.content.output_description,
                "note": self.content.note,
            },
            "author": {
                "user_uid": self.author.user_uid, 
                "handle": self.author.handle
            },
        }