from models import *
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_FILE}"
app.config['JWT_SECRET_KEY'] = 'Sidhant123'  # Replace with a strong secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)


# Part of Authentification. Register yourself with the database; the password you enter automatically gets hashed in the set_password method. Need to login next to get a token. This also makes sure
# that the username is not already taken.
@app.route('/api/register', methods=['POST'])
def register():
    req = request.get_json()
    username = req.get('username')
    name = req.get('name')
    major = req.get('major')
    penn_id = req.get('penn_id')
    graduation_year = req.get('graduation_year')
    password = req.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username is already taken'}), 400

    new_user = User(username=username, name=name, major=major, penn_id=penn_id,
                    graduation_year=graduation_year, interests=['Technology'], favorites=['penn-memes'])
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Once a user is registered, they can login to get a token. This token is used to authenticate the user for certain requests.
@app.route('/api/login', methods=['POST'])
def login():
    req = request.get_json()
    username = req.get('username')
    password = req.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.username)

    return jsonify({'access_token': access_token}), 200


@app.route('/')
def main():
    return "Welcome to Penn Club Review!"


@app.route('/api')
def api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

# Returns relevant club information for GET requests. Public for everyone, requires no user info/authentication.
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

# Makes a club with the given JSON information for POST requests, pretty standard stuff
def make_club():
    req = request.get_json()
    club_code, club_name = req.get('code'), req.get('name')
    club_description = req.get('description')
    club_tags = req.get('tags')
    new_club = Club(code=club_code, name=club_name,
                    description=club_description, tags=club_tags)
    db.session.add(new_club)
    db.session.commit()
    return club_name + " created successfully!"

# Returns a list of all clubs, or clubs that match the search parameter. You can also use the POST method to create a new club.
@app.route('/api/clubs', methods=['GET', 'POST'])
def clubs():
    if request.method == 'POST':
        return make_club()
    search_param = request.args.get('search')
    if search_param:
        search_clubs = Club.query.filter(Club.name.ilike(f"%{search_param}%"))
        return return_clubs(search_clubs)
    else:
        clubs = db.session.query(Club).all()
        return return_clubs(clubs)

# Allows you to modify information for an inputted club.
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

# Custon Route #1. Allows you to modify information about yourself. Requires authentification through JWT.
@app.route('/api/userinfo/<string:username>', methods=['PATCH'])
@jwt_required()
def modify_user_info(username):
    current_user_id = get_jwt_identity()
    # Ensure that the request is made by the user identified in the token
    if current_user_id != username:
        return jsonify({'message': 'Unauthorized access'}), 403
    req = request.get_json()
    user = User.query.filter_by(username=username).first()

    if user:
        for key, value in req.items():
            setattr(user, key, value)
        db.session.commit()

        return "Updated info for " + username
    else:
        return "User with username " + username + " not found", 404

# Displays cool, relevant, and public information for a user
@app.route('/api/user/<string:username>')
def show_profile(username):
    user = User.query.filter_by(username=username).first()
    return jsonify(username=user.username, name=user.name, major=user.major, graduation_year=user.graduation_year, interests=user.interests, favorites=user.favorites)

# Allows a user to add a club to their list of favorites. Requires authentification through JWT to make sure the user isn't just anyone.
# Accordingly adjusts their profile as well as the club they entered
@app.route('/api/<string:username>/favorite', methods=['POST'])
@jwt_required()
def favorite_club(username):
    current_user_id = get_jwt_identity()
    # Ensure that the request is made by the user identified in the token
    if current_user_id != username:
        return jsonify({'message': 'Unauthorized access'}), 403

    req = request.get_json()
    club_code = req.get('club_code')

    user_instance = User.query.get(username)
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
        club_instance.students_who_favored = [username]
    else:
        if username not in club_instance.students_who_favored:
            club_instance.students_who_favored.append(username)

    db.session.commit()

    return jsonify({"message": "Club favorited successfully"}), 200


# Method for getting a list of clubs by a given tag. Public for everyone, requires no user info/authentication.
@app.route('/api/tags', methods=['GET'])
def clubs_by_tag():
    tag = request.args.get('tag')

    clubs_with_tag = Club.query.filter(Club.tags.contains(tag)).all()

    if not clubs_with_tag:
        return jsonify({"message": "No clubs found with the specified tag"}), 404

    club_names = [club.name for club in clubs_with_tag]

    return jsonify({"Clubs with the " + tag + " include:": club_names}), 200


# Custon Route #2. Matches a user with clubs based on their interests and the clubs tag. Requires authentification through JWT.
@app.route('/api/match-with-clubs/<string:username>', methods=['GET'])
@jwt_required()
def clubs_by_user_interests(username):
    current_user_id = get_jwt_identity()
    if current_user_id != username:
        return jsonify({'message': 'Unauthorized access'}), 403

    user = User.query.get(username)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    user_interests = user.interests

    if not user_interests:
        return jsonify({"message": "User has no specified interests"}), 400

    matching_clubs = []

    for interest in user_interests:
        clubs_for_interest = Club.query.filter(
            Club.tags.contains(interest)).all()
        matching_clubs.extend(clubs_for_interest)

    if not matching_clubs:
        return jsonify({"message": "No matching clubs found"}), 404

    club_names = [club.name for club in matching_clubs]

    return jsonify({"Check out these clubs, they match with your interests: ": club_names}), 200


# Custom Route. Gets all reviews/comments for a given club. Public for everyone, requires no user info/authentication.
@app.route('/api/clubs/<string:code>/comments', methods=['GET'])
def get_club_comments(code):
    club = Club.query.filter_by(code=code).first()

    if club is None:
        return jsonify({"message": "Club not found"}), 404

    comments = ClubComment.query.filter_by(
        club_code=code, parent_comment_id=None).all()
    comments_data = []

    for comment in comments:
        comment_info = {
            "id": comment.id,
            "user_username": comment.user_username,
            "text": comment.text,
            "timestamp": comment.timestamp.isoformat(),
            "replies": []
        }

        replies = ClubComment.query.filter_by(
            parent_comment_id=comment.id).all()
        for reply in replies:
            reply_info = {
                "id": reply.id,
                "user_username": reply.user_username,
                "text": reply.text,
                "timestamp": reply.timestamp.isoformat()
            }
            comment_info["replies"].append(reply_info)

        comments_data.append(comment_info)

    return jsonify({"club_comments": comments_data}), 200

# Custom Route. Allows a user to add a comment to a club. Requires authentification through JWT.
@app.route('/api/clubs/<string:code>/comments', methods=['POST'])
@jwt_required()
def add_club_comment(code):
    current_user_id = get_jwt_identity()
    req = request.get_json()
    comment_text = req.get('text')

    club = Club.query.filter_by(code=code).first()

    if club is None:
        return jsonify({"message": "Club not found"}), 404

    new_comment = ClubComment(
        club_code=code,
        user_username=current_user_id,
        text=comment_text
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully"}), 201


if __name__ == '__main__':
    app.run()
