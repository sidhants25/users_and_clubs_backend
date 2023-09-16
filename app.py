from flask import Flask, jsonify
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


@app.route('/clubs', methods=['GET'])
def clubs():
    clubs = Club.query.all()
    return jsonify({"all clubs": [club.serialize() for club in clubs]})


if __name__ == '__main__':
    app.run()
