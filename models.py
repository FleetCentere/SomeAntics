from ProjectFiles import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class pressReleases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(250))
    ticker = db.Column(db.String(10))
    link = db.Column(db.String(100))
    product = db.Column(db.String(50))
    datePosted = db.Column(db.Date, index=True)

    def __repr__(self):
        return f"{self.company}: {self.product} on {self.datePosted}"

class events(db.Model):
    # for events like exercise, meetings
    id = db.Column(db.Integer, primary_key=True)
    eventType = db.Column(db.String(50))
    eventDatetime = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    duration = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.eventType} on {self.eventDate}"

class content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentType = db.Column(db.String(50)) # podcast, movies, shows, youtube, articles
    contentCreator = db.Column(db.String(100))
    dateMade = db.Column(db.Date)
    link = db.Column(db.String(300))
    dateConsumed = db.Column(db.Date, index=True)

    def __repr__(self):
        return f"{self.contentType} by {self.contentCreator}"

class people(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(50))
    place = db.Column(db.String(100))
    date = db.Column(db.Date)

    def __repr__(self):
        return f"{self.person} on {self.date}"
