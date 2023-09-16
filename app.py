from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)

from models import *


@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

def return_clubs(clubs):
    return_list = []
    for club in clubs:
        club_info = {
            'name': club.name,
            'code': club.code,
            'description': club.description,
            'tags': club.tags
        }
        return_list.append(club_info)
    return jsonify(return_list)

@app.route('/api/clubs', methods=['GET'])
def clubs():
    clubs = db.session.query(Club).all()
    return return_clubs(clubs)

@app.route('/api/user/<string:username>')
def show_profile(username):
    user = User.query.filter_by(username=username).first()
    return jsonify(username=user.username, name = user.name, major = user.major, graduation_year = user.graduation_year, interests = user.interests)

if __name__ == '__main__':
    app.run()
