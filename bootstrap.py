import os
from app import db, DB_FILE
from users import User
from models import *
import json

def create_user():
        josh = User(penn_id=12345678, name='Josh', major='Computer Science', graduation_year='2026', interests=['Software', 'Singing', 'Poker'])
        db.session.add(josh)
        db.session.commit()

def load_data():
        with open('clubs.json', 'r') as json_file:
            data = json.load(json_file)
            
            for club_info in data:
                club = Club(
                    code=club_info['code'],
                    name=club_info['name'],
                    description=club_info['description'],
                    tags=club_info['tags']
                )
                db.session.add(club)
            
            db.session.commit()



# No need to modify the below code.
if __name__ == '__main__':
    # Delete any existing database before bootstrapping a new one.
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    db.create_all()
    create_user()
    load_data()
