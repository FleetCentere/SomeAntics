from ProjectFiles import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# userTable, taskTable, newsTable, eventTable, contentTable, peopleTable, exerciseTable, weightTable, companyTable

@login.user_loader
def load_user(id):
    return userTable.query.get(int(id))

class userTable(UserMixin, db.Model):
    # for users of the website
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    name = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120))
    
    # referenced tables
    tasks = db.relationship("taskTable", backref="author", lazy="dynamic")
    news = db.relationship("newsTable", backref="author", lazy="dynamic")
    events = db.relationship("eventTable", backref="author", lazy="dynamic")
    contents = db.relationship("contentTable", backref="author", lazy="dynamic")
    people = db.relationship("peopleTable", backref="author", lazy="dynamic")
    exercise = db.relationship("exerciseTable", backref="author", lazy="dynamic")
    weight = db.relationship("weightTable", backref="author", lazy="dynamic")
    company = db.relationship("companyTable", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f"<User {self.username}>"

class taskTable(db.Model):
    # tasks and items to do including personal, content to read
    id = db.Column(db.Integer, primary_key=True)
    taskCategory = db.Column(db.String(250))
    taskName = db.Column(db.String(250))
    taskLink = db.Column(db.String(200))
    taskNote = db.Column(db.Text)
    taskStatus = db.Column(db.String(50), default="New")
    dateEntered = db.Column(db.Date, default=datetime.utcnow)
    dateEdited = db.Column(db.Date, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))

    def __repr__(self):
        return f"{self.taskName} on {self.dateEntered}"

class newsTable(db.Model):
    # for news including press releases, sports, politics, global, tech, finance, etc.
    id = db.Column(db.Integer, primary_key=True)
    newsType = db.Column(db.String(50))
    newsTitle = db.Column(db.String(50))
    newsNote = db.Column(db.Text)
    newsLink = db.Column(db.String(200))
    newsTicker = db.Column(db.String(10))
    newsDatePosted = db.Column(db.Date)
    newsDateEntered = db.Column(db.Date, default=datetime.utcnow)
    company = db.relationship("companyTable", backref="news", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))
    
    def __repr__(self):
        return f"{self.newsType}: {self.newsTitle} on {self.newsDatePosted}"

class eventTable(db.Model):
    # for events like exercise, meetings, golf
    id = db.Column(db.Integer, primary_key=True)
    eventType = db.Column(db.String(50))
    eventDatetime = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    eventLocation = db.Column(db.String(50))
    eventNote = db.Column(db.Text)
    exercises = db.relationship("exerciseTable", backref="event", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))

    def __repr__(self):
        return f"{self.eventType} on {self.eventDate}"

class contentTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dateConsumed = db.Column(db.Date, default=datetime.utcnow, index=True)
    dateMade = db.Column(db.Date)
    contentType = db.Column(db.String(50)) # podcast, movies, shows, youtube, articles
    contentCreator = db.Column(db.String(100))
    contentLink = db.Column(db.String(200))
    contentRating = db.Column(db.Integer)
    contentSubject = db.Column(db.String(200))
    contentNote = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))

    def __repr__(self):
        return f"{self.contentType} by {self.contentCreator} about {self.contentSubject}"

class peopleTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(50))
    place = db.Column(db.String(100))
    date = db.Column(db.Date)
    note = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))

    def __repr__(self):
        return f"{self.person} on {self.date}"

class exerciseTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exerciseDuration = db.Column(db.Integer)
    exerciseType = db.Column(db.String(50))
    exerciseDistance = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event_table.id"))
    
class weightTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weightDate = db.Column(db.Date, default=datetime.utcnow, index=True)
    weight = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))

class companyTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    companyPost = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))
    news_id = db.Column(db.Integer, db.ForeignKey("news_table.id"))