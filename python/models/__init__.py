import enum
from database import db
from sqlalchemy.sql.functions import current_timestamp


class SubmissionVerdict(enum.Enum):
    PENDING = -1
    ACCEPTED = 0
    WRONG_ANSWER = 1
    TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3


class User(db.Model):  # type: ignore[name-defined]
    user_uid = db.Column(db.String(36), primary_key=True)
    handle = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    email_verified = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.CheckConstraint(email_verified.in_({0, 1})),)


class Profile(db.Model):  # type: ignore[name-defined]
    user_uid = db.Column(
        db.ForeignKey(User.user_uid, ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    img_type = db.Column(db.String(5), default=None)
    email = db.Column(db.String(100), default=None)
    school = db.Column(db.String(100), default=None)
    bio = db.Column(db.String(100), default=None)


class ProblemChecker(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)


class ProblemSolution(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)


class Problem(db.Model):  # type: ignore[name-defined]
    problem_id = db.Column(db.Integer, primary_key=True, nullable=False)
    problem_token = db.Column(db.String(100), unique=True, nullable=False)
    problem_author = db.Column(
        db.ForeignKey(User.user_uid, ondelete="CASCADE", onupdate="CASCADE")
    )
    problem_checker = db.Column(
        db.ForeignKey(ProblemChecker.id, ondelete="CASCADE", onupdate="CASCAde")
    )
    problem_solution = db.Column(
        db.ForeignKey(ProblemSolution.id, ondelete="CASCADE", onupdate="CASCADE")
    )


class VerdictErrorComment(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    failed_testcase_index = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(100), nullable=False)


class Verdict(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    tracker_uid = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=current_timestamp(), nullable=False)
    verdict = db.Column(db.String(100), nullable=False)
    error_id = db.Column(db.ForeignKey(VerdictErrorComment.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    memory_usage = db.Column(db.Integer, nullable=False)
    time_usage = db.Column(db.Integer, nullable=False)


class Submission(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_uid = db.Column(
        db.ForeignKey(User.user_uid), nullable=False
    )
    problem_id = db.Column(
        db.ForeignKey(Problem.problem_id), nullable=False
    )
    date = db.Column(db.DateTime, default=current_timestamp(), nullable=False)
    compiler = db.Column(db.String(100), nullable=False)
    tracker_uid = db.Column(db.ForeignKey(Verdict.tracker_uid), nullable=True)