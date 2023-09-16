import os
from app import app, db, DB_FILE
from models import *
import json

def create_user():
    # with app.app_context():
    josh = User(username = 'josh_iz_da_best', penn_id=12345678, name='Josh', major='Computer Science', graduation_year='2026', interests=['Athletics', 'Technology', 'Poker'], favorites= ['pppjo'])
    db.session.add(josh)
    db.session.commit()


def load_data():
    # with app.app_context():
    with open('clubs.json', 'r') as json_file:
        data = json.load(json_file)
        
        for club_info in data:
            club = Club(
                code=club_info['code'],
                name=club_info['name'],
                description=club_info['description'],
                tags = club_info['tags'],
            )
            db.session.add(club)
        
        db.session.commit()



# No need to modify the below code.
if __name__ == '__main__':
    with app.app_context():
        # print('hi')
        # print(DB_FILE)
        # app.app_context()
        # Delete any existing database before bootstrapping a new one.
        if os.path.exists('instance/' + DB_FILE):
            print('no hi')
            os.remove('instance/' + DB_FILE)

            db.create_all()
            create_user()
            # print("Debugging...")
            load_data()
        else:
            print('didnt')
