# Penn Users and Clubs Backend Model

## Documentation

I. Defining Models

I defined fairly standard attributes for both Clubs and Users in models.py. One cool feature I added was for a User to define a list of their interests; this came in handy when
I created a method that matched a User to clubs based on their list of interests. To store interests + favorites for Users — as well as tags and students_who_favored for Clubs — I used a
JSON column due to its conveniance and accessibility.

II. Bootstrap

I created an account for Josh, "josh_iz_da_best" and filled out some of his information. For load_data, I iterated through each club's information in clubs.json and added a corresponding club
to the database. I wasn't able to get the pipenv run python bootstrap.py command working because of a the file path was mislabeled. However, thanks to some great debugging work by Justin, I finally got the database bootstrapped and running.

III. Default Routes

Overall, I thought most of the provided routes were pretty straightforward to implement. I defined a few helper functions that I was able to utilize throughout various routes + requests. For instance, the return_clubs method just takes in a list of clubs and adds the relevant information for each club in a JSON format. One thing I thought about in particular was the favorite a club route. I wanted to make sure that the action would be reflected in both the student's list of favorite clubs as well as the club's list of favorite students. I took care of both things in my method.

IV. Custom Routes!

I really enjoyed this section as I was able to implement ideas that I thought would be a neat addition for the system. The first route I created was a "match with clubs" route which looks 
through a user's interests and returns all clubs that have at least one tag corresponding to those interests. I thought this would be a great feature to have from a user standpoint as it would save them from the time of having to go through all the clubs. It also helps promote clubs for their intended audiences. The second route I created was a modify user route which was analogous to the modify clubs route. I felt this was an important feature to have, especially after implementing authentification.

I also added two more routes for authentification (see below)

V. Authentification - JSON Web Tokens 

As a user of many websites/products, I understand the importance of data privacy and security. Thus, I used JSON Web Tokens (JWT), a pretty high level of user authentification to ensure that all important information was stored securely and that certain routes were restricted. I created a register section where users can sign up for the app. Their password is then hashed through the set_password method in models. Once the user registers, they have to log in and obtain an access token.

Certain routes (such as 'match with clubs', editing user info, and favoriting clubs) are jwt required, meaning the user needs to provide their unique access token in the autherization header. I thought this was a secure and robust way to make sure that user information is protected and private.

If I had more time, I would have implemented autherization for clubs, where only certain admins would be able to edit/add/delete club information.

VI. Bonus Features

I implemented club comments through adding a new model and two routes. The ClubComment model uses two relationships for the commentor and the associated club. I also used a reltionship to support a thread: each comment reply has a parent/original comment. I'm able to store important parts of the comment, such as the commentor's username, their actual comment, and the time stamp of the comment. I added two new routes in the app.py section, one public route for getting comments for a certain club and one private route (JWT required) for posting/replying to a comment.

VII. Final Thoughts & Reflections

Overall, I really enjoyed working on this project (apart from the tedious time-to-time debugging) and learned a few new skills in Flask. Thanks for considering me for Penn Labs!
## Installation

1. Click the green "use this template" button to make your own copy of this repository, and clone it. Make sure to create a **private repository**.
2. Change directory into the cloned repository.
3. Install `pipenv`
   - `pip install --user --upgrade pipenv`
4. Install packages using `pipenv install`.

## File Structure

- `app.py`: Main file. Has configuration and setup at the top. Add your [URL routes](https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing) to this file!
- `models.py`: Model definitions for SQLAlchemy database models. Check out documentation on [declaring models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) as well as the [SQLAlchemy quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart) for guidance
- `bootstrap.py`: Code for creating and populating your local database. You will be adding code in this file to load the provided `clubs.json` file into a database.

## Developing

0. Determine how to model the data contained within `clubs.json` and then complete `bootstrap.py`
1. Run `pipenv run python bootstrap.py` to create the database and populate it.
2. Use `pipenv run flask run` to run the project.
3. Follow the instructions [here](https://www.notion.so/pennlabs/Backend-Challenge-Fall-20-31461f3d91ad4f46adb844b1e112b100).
4. Document your work in this `README.md` file.

## Submitting

Follow the instructions on the Technical Challenge page for submission.

## Installing Additional Packages

Use any tools you think are relevant to the challenge! To install additional packages
run `pipenv install <package_name>` within the directory. Make sure to document your additions.
