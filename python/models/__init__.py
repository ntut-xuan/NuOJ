from database import db

class User(db.Model):
    user_uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    handle = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    email_verified = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (db.CheckConstraint(email_verified.in_({0, 1})),)
