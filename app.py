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

#Returns relevant club information for GET requests
def return_clubs(clubs):
    return_list = []
    for club in clubs:
        club_info = {
            'name': club.name,
            'code': club.code,
            'description': club.description,
            'tags': club.tags,
            'students_who_favored': club.students_who_favored
        }
        return_list.append(club_info)
    return jsonify(return_list)

#Makes a club with the given JSON information for POST requests, pretty standard stuff
def make_club():
    req = request.get_json()
    club_code, club_name = req.get('code'), req.get('name')
    club_description = req.get('description')
    club_tags = req.get('tags')
    new_club = Club(code=club_code, name=club_name, description=club_description, tags=club_tags)
    db.session.add(new_club)
    db.session.commit()
    return club_name + " created successfully!"

#Returns a list of all clubs, or clubs that match the search parameter. You can also use the POST method to create a new club.
@app.route('/api/clubs', methods=['GET', 'POST'])
def clubs():
        if request.method == 'POST':
            return make_club()
        search_param = request.args.get('search')
        if search_param:
            search_clubs = Club.query.filter(Club.name.ilike(f"%{search_param}%"))
            print(search_clubs)
            return return_clubs(search_clubs)
        else:
             clubs = db.session.query(Club).all()
             return return_clubs(clubs)
    
#Allows you to modify information for an inputted club
@app.route('/api/clubs/<string:code>', methods=['PATCH'])
def modify_club_info(code):
    req = request.get_json()
    club = Club.query.filter_by(code=code).first()
    
    if club:
        for key, value in req.items():
            setattr(club, key, value)
        db.session.commit()
        
        return "Updated info for " + code 
    else:
        return "Club with code " + code + " not found", 404

#Displays cool, relevant, and public (can't be exposing info) information for a user
@app.route('/api/user/<string:username>')
def show_profile(username):
    user = User.query.filter_by(username=username).first()
    return jsonify(username=user.username, name = user.name, major = user.major, graduation_year = user.graduation_year, interests = user.interests, favorites = user.favorites)

#Allows a user to add a club to their list of favorites. Accordingly adjusts their profile as well as the club they entered
@app.route('/api/<string:user>/favorite', methods=['POST'])
def favorite_club(user):
    req = request.get_json()
    club_code = req.get('club_code')

    user_instance = User.query.get(user)
    club_instance = Club.query.get(club_code)

    if user_instance is None:
        return jsonify({"error": "User not found"}), 404
    if club_instance is None:
        return jsonify({"error": "Club not found"}), 404

    if user_instance.favorites is None:
        user_instance.favorites = [club_code]
    else:
        if club_code not in user_instance.favorites:
            user_instance.favorites.append(club_code)

    if club_instance.students_who_favored is None:
        club_instance.students_who_favored = [user]
    else:
        if user not in club_instance.students_who_favored:
            club_instance.students_who_favored.append(user)

    db.session.commit()

    return jsonify({"message": "Club favorited successfully"}), 200


#Method for getting a list of clubs by a given tag
@app.route('/api/tags', methods=['GET'])
def clubs_by_tag():
    tag = request.args.get('tag')
    print(tag)

    clubs_with_tag = Club.query.filter(Club.tags.contains(tag)).all()
    print(clubs_with_tag)

    if not clubs_with_tag:
        return jsonify({"message": "No clubs found with the specified tag"}), 404

    club_names = [club.name for club in clubs_with_tag]

    return jsonify({"Clubs with the " + tag + " include:": club_names}), 200


#My own route. Matches a user with clubs based on their interests and the clubs tag.
@app.route('/api/match-with-clubs/<string:username>', methods=['GET'])
def clubs_by_user_interests(username):
    user = User.query.get(username)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    user_interests = user.interests

    if not user_interests:
        return jsonify({"message": "User has no specified interests"}), 400

    matching_clubs = []

    for interest in user_interests:
        clubs_for_interest = Club.query.filter(Club.tags.contains(interest)).all()
        matching_clubs.extend(clubs_for_interest)
    
    print(matching_clubs)
    

    if not matching_clubs:
        return jsonify({"message": "No matching clubs found"}), 404

    club_names = [club.name for club in matching_clubs]

    return jsonify({"Check out these clubs, they match with your interests: ": club_names}), 200


if __name__ == '__main__':
    app.run()
