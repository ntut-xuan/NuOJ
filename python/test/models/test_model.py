from datetime import datetime
from uuid import uuid4

import pytest
from flask import Flask
from sqlalchemy.sql import null

from database import db
from models import Language, Problem, ProblemChecker, ProblemSolution, Profile, Submission, Testcase, Verdict, VerdictErrorComment, User


@pytest.fixture
def setup_user(app: Flask):
    with app.app_context():
        user: User = User(
            user_uid="some-random-uuid",
            handle="some-handle",
            password="some-password",
            email="test@email.com",
            role=1,
            email_verified=1,
        )

        db.session.add(user)
        db.session.commit()


@pytest.fixture
def setup_problem(app: Flask, setup_user: None):
    with app.app_context():
        problem: Problem = Problem(
            problem_id=1,
            problem_token="some-random-token",
            problem_author="some-random-uuid",
        )

        db.session.add(problem)
        db.session.commit()


@pytest.fixture
def setup_language(app: Flask):
    with app.app_context():
        language: Language = Language(
            name="C++14",
            extension="cpp"
        )

        db.session.add(language)
        db.session.commit()


def test_user_model_with_valid_data_should_add_record_to_database(
    app: Flask, setup_user: None
):
    with app.app_context():

        user_from_database: User | None = User.query.filter(
            User.user_uid == "some-random-uuid"
        ).first()
        assert user_from_database is not None
        assert user_from_database.user_uid == "some-random-uuid"
        assert user_from_database.handle == "some-handle"
        assert user_from_database.password == "some-password"
        assert user_from_database.email == "test@email.com"
        assert user_from_database.role == 1
        assert user_from_database.email_verified == 1


def test_profile_model_with_valid_data_should_add_record_to_database(
    app: Flask, setup_user: None
):
    with app.app_context():
        profile: Profile = Profile(
            user_uid="some-random-uuid",
            img_type=None,
            email=None,
            school=None,
            bio=None,
        )

        db.session.add(profile)
        db.session.commit()

        profile_from_database: Profile | None = Profile.query.filter(
            Profile.user_uid == "some-random-uuid"
        ).first()
        assert profile_from_database is not None
        assert profile_from_database.user_uid == "some-random-uuid"
        assert profile_from_database.bio == None
        assert profile_from_database.email == None
        assert profile_from_database.img_type == None
        assert profile_from_database.school == None


def test_problem_model_with_valid_data_should_add_record_to_database(
    app: Flask, setup_problem: None
):
    with app.app_context():

        problem_from_database: Problem | None = Problem.query.filter(
            Problem.problem_id == 1
        ).first()
        assert problem_from_database is not None
        assert problem_from_database.problem_author == "some-random-uuid"
        assert problem_from_database.problem_id == 1
        assert problem_from_database.problem_token == "some-random-token"


def test_submission_model_with_valid_data_should_add_record_to_database(
    app: Flask, setup_user: None, setup_problem: None
):
    with app.app_context():
        specific_datetime: datetime = datetime.now()
        code_uid: str = str(uuid4())
        submission: Submission = Submission(
            id=1,
            user_uid="some-random-uuid",
            problem_id=1,
            date=specific_datetime,
            compiler="C++14",
            code_uid=code_uid,
            tracker_uid=None
        )

        db.session.add(submission)
        db.session.commit()

        submission_from_database: Submission | None = Submission.query.filter(
            Submission.id == 1
        ).first()
        assert submission_from_database is not None
        assert submission_from_database.id == 1
        assert submission_from_database.user_uid == "some-random-uuid"
        assert submission_from_database.problem_id == 1
        assert submission_from_database.date == specific_datetime
        assert submission_from_database.compiler == "C++14"
        assert submission_from_database.code_uid == code_uid
        assert submission_from_database.tracker_uid == None


def test_verdict_model_with_valid_data_should_add_record_to_database(app: Flask):
    with app.app_context():
        specific_datetime: datetime = datetime.now()
        verdict: Verdict = Verdict(
            id=1,
            tracker_uid="some-random-uuid",
            date=specific_datetime,
            verdict="Accepted",
            error_id=None,
            memory_usage=100000,
            time_usage=3014
        )

        db.session.add(verdict)
        db.session.commit()

        verdict_from_database: Verdict | None = Verdict.query.filter(Verdict.id == 1).first()
        assert verdict_from_database is not None
        assert verdict_from_database.verdict == "Accepted"
        assert verdict_from_database.tracker_uid == "some-random-uuid"
        assert verdict_from_database.date == specific_datetime
        assert verdict_from_database.error_id == None
        assert verdict_from_database.memory_usage == 100000
        assert verdict_from_database.time_usage == 3014


def test_verdict_error_message_model_with_valid_data_should_add_record_to_database(app: Flask):
    with app.app_context():
        verdict_error_comment: VerdictErrorComment = VerdictErrorComment(
            id=1,
            failed_testcase_index=5,
            message="Wrong answer expected 9 but got 8."
        )

        db.session.add(verdict_error_comment)
        db.session.commit()

        verdict_error_comment_from_database: VerdictErrorComment | None = VerdictErrorComment.query.filter(VerdictErrorComment.id == 1).first()
        assert verdict_error_comment_from_database is not None
        assert verdict_error_comment_from_database.failed_testcase_index == 5
        assert verdict_error_comment_from_database.message == "Wrong answer expected 9 but got 8."


def test_problem_checker_model_with_valid_data_should_add_record_to_database(app: Flask):
    with app.app_context():
        random_filename: str = "5b3e4966-09cf-40be-9059-55fa656ba45a"
        problem_checker: ProblemChecker = ProblemChecker(
            id=1,
            filename=random_filename
        )

        db.session.add(problem_checker)
        db.session.commit()

        problem_checker_from_database: ProblemChecker | None = ProblemChecker.query.filter_by(id=1).first()
        assert problem_checker_from_database is not None
        assert problem_checker_from_database.filename == random_filename


def test_problem_solution_model_with_valid_data_should_add_record_to_database(app: Flask, setup_language: None):
    with app.app_context():
        random_filename: str = "5b3e4966-09cf-40be-9059-55fa656ba45a"
        problem_checker: ProblemSolution = ProblemSolution(
            id=1,
            language= "C++14",
            filename=random_filename
        )

        db.session.add(problem_checker)
        db.session.commit()

        problem_checker_from_database: ProblemSolution | None = ProblemSolution.query.filter_by(id=1).first()
        assert problem_checker_from_database is not None
        assert problem_checker_from_database.language == "C++14"
        assert problem_checker_from_database.filename == random_filename


def test_language_model_with_valid_data_should_add_record_to_database(app: Flask):
    with app.app_context():
        language: Language = Language(
            name="C++14",
            extension="cpp"
        )

        db.session.add(language)
        db.session.commit()

        language_from_database: Language | None = Language.query.filter_by(name="C++14").first()
        assert language_from_database is not None
        assert language_from_database.extension == "cpp"


def test_testcase_model_with_valid_data_should_add_record_to_database(app: Flask):
    with app.app_context():
        random_filename: str = "5b3e4966-09cf-40be-9059-55fa656ba45a"
        testcase: Testcase = Testcase(
            id=1,
            filename=random_filename
        )

        db.session.add(testcase)
        db.session.commit()

        testcase_from_database: Testcase | None = Testcase.query.filter_by(id=1).first()
        assert testcase_from_database is not None
        assert len(testcase_from_database.filename) == len(random_filename)