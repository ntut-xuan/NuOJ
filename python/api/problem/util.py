import json
from typing import Any

from api.problem.dataclass import ProblemContent, ProblemData, ProblemHead
from models import Problem, User
from storage.util import TunnelCode, read_file


def get_problem_file_data_with_problem_token(problem_token: str) -> dict[str, Any]:
    problem_raw_data: str = read_file(f"{problem_token}.json", TunnelCode.PROBLEM)
    problem_dict: dict[str, Any] = json.loads(problem_raw_data)

    return problem_dict

def get_problem_data_object_with_problem_pid(problem_pid: str) -> ProblemData:
    problem: Problem | None = Problem.query.filter_by(problem_id=problem_pid).first()
    assert problem is not None

    problem_id: str = problem.problem_id
    problem_token: str = problem.problem_token
    problem_author: str = problem.problem_author

    user: User | None = User.query.filter_by(user_uid=problem_author).first()
    assert user is not None

    problem_dict = get_problem_file_data_with_problem_token(problem_token)
    problem_dict["head"] |= {"problem_pid": problem_id}

    problem_data: ProblemData = ProblemData(
        content=ProblemContent(**problem_dict["content"]),
        head=ProblemHead(**problem_dict["head"]),
        author=user,
    )

    return problem_data