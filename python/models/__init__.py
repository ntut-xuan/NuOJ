from database import db


class User(db.Model): # type: ignore[name-defined]
    user_uid = db.Column(db.String(36), primary_key=True)
    handle = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    email_verified = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.CheckConstraint(email_verified.in_({0, 1})),)


class Profile(db.Model): # type: ignore[name-defined]
    user_uid = db.Column(
        db.ForeignKey(User.user_uid, ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    img_type = db.Column(db.String(5), default=None)
    email = db.Column(db.String(100), default=None)
    school = db.Column(db.String(100), default=None)
    bio = db.Column(db.String(100), default=None)
