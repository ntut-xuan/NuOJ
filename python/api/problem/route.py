from dataclasses import dataclass
from http import HTTPStatus
from json import loads
from typing import Any

from flask import Blueprint, Response, make_response

from models import Problem, User
from storage.util import TunnelCode, read_file
from util import make_simple_error_response

problem_bp = Blueprint("problem", __name__, url_prefix="/api/problem")


@dataclass
class ProblemContent:
    title: str
    description: str
    input_description: str
    output_description: str
    note: str


@dataclass
class ProblemSetting:
    time_limit: float
    memory_limit: float


@dataclass
class ProblemData:
    content: ProblemContent
    basic_setting: ProblemSetting
    problem_pid: str
    author: User

    def __dict__(self):
        return {
            "head": {
                "title": self.content.title,
                "problem_pid": self.problem_pid,
                "time_limit": self.basic_setting.time_limit,
                "memory_limit": self.basic_setting.memory_limit,
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


@problem_bp.route("/<int:id>/", methods=["GET"])
def get_problems_data_route(id: int) -> Response:
    problem: Problem | None = Problem.query.filter_by(problem_id=id).first()

    if problem is None:
        return make_simple_error_response(
            HTTPStatus.FORBIDDEN, "The problem with the specific ID is not found."
        )

    problem_token: str = problem.problem_token
    problem_author: str = problem.problem_author

    problem_data: ProblemData = __get_problem_data_with_problem_token(
        problem_token, problem_author
    )

    return make_response(problem_data.__dict__())


@problem_bp.route("/", methods=["GET"])
def get_all_problems_data_route() -> Response:
    problems: list[Problem] = Problem.query.all()

    payload: dict[str, Any] = {
        "count": len(problems),
        "result": [
            {
                "id": problem.problem_id,
                "data": __get_problem_data_with_problem_token(
                    problem.problem_token, problem.problem_author
                ).__dict__(),
            }
            for problem in problems
        ],
    }

    return make_response(payload)


def __get_problem_data_with_problem_token(
    problem_token: str, problem_author: str, problem_pid: str
) -> ProblemData:
    problem_raw_data: str = read_file(f"{problem_token}.json", TunnelCode.PROBLEM)
    problem_dict: dict[str, Any] = loads(problem_raw_data)
    user: User | None = User.query.filter_by(user_uid=problem_author).first()

    assert user is not None

    problem_data: ProblemData = ProblemData(
        content=ProblemContent(**problem_dict["problem_content"]),
        basic_setting=ProblemSetting(**problem_dict["basic_setting"]),
        problem_pid=problem_pid,
        author=user,
    )

    return problem_data
