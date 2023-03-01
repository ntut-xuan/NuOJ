import pytest
from flask import Flask

from database import db
from models import Problem, Profile, Submission, SubmissionVerdict, User


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
    app: Flask, setup_problem: None
):
    with app.app_context():
        submission: Submission = Submission(
            submission_id=1,
            problem_id=1,
            user_uid="some-random-uuid",
            verdict=SubmissionVerdict.ACCEPTED,
            time=1.1,
            memory=32767,
        )

        db.session.add(submission)
        db.session.commit()

        submission_from_database: Submission | None = Submission.query.filter(
            Submission.submission_id == 1
        ).first()
        assert submission_from_database.submission_id == 1
        assert submission_from_database.problem_id == 1
        assert submission_from_database.time == 1.1
        assert submission_from_database.memory == 32767
