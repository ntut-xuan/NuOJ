import enum
from database import db


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


class Problem(db.Model):  # type: ignore[name-defined]
    problem_id = db.Column(db.Integer, primary_key=True, nullable=False)
    problem_token = db.Column(db.String, unique=True, nullable=False)
    problem_author = db.Column(
        db.ForeignKey(User.user_uid, ondelete="CASCADE", onupdate="CASCADE")
    )


class Submission(db.Model):  # type: ignore[name-defined]
    submission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    problem_id = db.Column(
        db.ForeignKey(Problem.problem_id, ondelete="CASCADE", onupdate="CASCADE")
    )
    user_uid = db.Column(
        db.ForeignKey(User.user_uid, ondelete="CASCADE", onupdate="CASCADE")
    )
    verdict = db.Column(db.Enum(SubmissionVerdict), default=SubmissionVerdict.PENDING)
    time = db.Column(db.Float, default=None)
    memory = db.Column(db.Float, default=None)
