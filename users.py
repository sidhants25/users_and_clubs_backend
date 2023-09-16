from app import db
from sqlalchemy import ARRAY
from sqlalchemy import CheckConstraint



class User(db.Model):
    penn_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    major = db.Column(db.String(100), unique=False, nullable=True)
    graduation_year = db.Column(db.String(4), unique=False, nullable=False)
    interests = db.Column(ARRAY(db.String(20)), nullable=True)


__table_args__ = (
        CheckConstraint('LENGTH(CAST(penn_id AS TEXT)) = 8', name='check_penn_id_length'),
    )