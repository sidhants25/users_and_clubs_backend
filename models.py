from app import db
from sqlalchemy import ARRAY


class Club(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False, default='')
    tags = db.Column(ARRAY(db.String), nullable=True)

    def __repr__(self):
        return '<Club %r>' % self.code



# Your database models should go here.
# Check out the Flask-SQLAlchemy quickstart for some good docs!
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
