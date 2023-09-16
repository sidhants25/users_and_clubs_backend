from app import db
from sqlalchemy import JSON


class Club(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False, default='')
    tags = db.Column(JSON)
    students_who_favored = db.Column(JSON)


class User(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    penn_id = db.Column(db.Integer(), nullable=False, unique=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    major = db.Column(db.String(100), unique=False, nullable=True)
    graduation_year = db.Column(db.String(4), unique=False, nullable=False)
    interests = db.Column(JSON)
    favorites = db.Column(JSON)


# __table_args__ = (
#         CheckConstraint('LENGTH(CAST(penn_id AS TEXT)) = 8', name='check_penn_id_length'),
#     )


# Your database models should go here.
# Check out the Flask-SQLAlchemy quickstart for some good docs!
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
