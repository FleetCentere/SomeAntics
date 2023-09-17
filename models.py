from ProjectFiles import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# userTable, dayTable, taskTable, newsTable, eventTable, contentTable, personsTable, exerciseTable, ideaTable, sourcesTable

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
    persons = db.relationship("personsTable", backref="author", lazy="dynamic")
    exercises = db.relationship("exerciseTable", backref="author", lazy="dynamic")
    days = db.relationship("dayTable", backref="author", lazy="dynamic")
    # peopleEvents = db.relationship("peopleEvents", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f"<User {self.username}>"

class dayTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float)
    sleep = db.Column(db.String(50))
    morning = db.Column(db.Text)
    afternoon = db.Column(db.Text)
    evening = db.Column(db.Text)
    journal = db.Column(db.Text)
    events = db.relationship("eventTable", backref="day", lazy="dynamic")
    contents = db.relationship("contentTable", backref="day", lazy="dynamic")
    news = db.relationship("newsTable", backref="day", lazy="dynamic")
    exercises = db.relationship("exerciseTable", backref="day", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id", name="fk_user_day"))

    def __repr__(self):
        return f"{self.date}"

class taskTable(db.Model):  
    # tasks and items to do including personal, content to read
    id = db.Column(db.Integer, primary_key=True)
    taskCategory = db.Column(db.String(250))
    taskName = db.Column(db.String(250))
    taskLink = db.Column(db.String(200))
    taskNote = db.Column(db.Text)
    taskStatus = db.Column(db.String(50), default="New")
    dateEntered = db.Column(db.Date, default=datetime.now())
    dateEdited = db.Column(db.Date, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id", name="fk_user_task"))

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
    newsDateEntered = db.Column(db.Date, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id", name="fk_user_news"))
    day_id = db.Column(db.Integer, db.ForeignKey("day_table.id", name="fk_day_news"))
    
    def __repr__(self):
        return f"{self.newsType}: {self.newsTitle} on {self.newsDatePosted}"

class eventTable(db.Model):
    # for events like exercise, meetings, golf
    id = db.Column(db.Integer, primary_key=True)
    eventType = db.Column(db.String(50))
    eventTime = db.Column(db.Time)
    eventLocation = db.Column(db.String(50))
    eventNote = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id", name="fk_user_event"))
    day_id = db.Column(db.Integer, db.ForeignKey("day_table.id", name="fk_day_event"))

    # eventDatetime = db.Column(db.DateTime, default=datetime.now(), index=True)

    def __repr__(self):
        return f"{self.eventType} on {self.eventDate}"

class contentTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentComplete = db.Column(db.Boolean)
    dateConsumed = db.Column(db.Date)
    dateMade = db.Column(db.Date)
    contentType = db.Column(db.String(50)) # podcast, movies, shows, youtube, articles
    contentCreator = db.Column(db.String(100))
    contentLink = db.Column(db.String(200))
    contentRating = db.Column(db.Integer)
    contentSubject = db.Column(db.String(200))
    contentNote = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id", name="fk_user_content"))
    day_id = db.Column(db.Integer, db.ForeignKey("day_table.id", name="fk_day_content"))

    def __repr__(self):
        return f"{self.contentType} by {self.contentCreator} about {self.contentSubject}"

class personsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id", name="fk_user_persons"))
    person = db.Column(db.String(50))
    personBackground = db.Column(db.Text)
    personBirthday = db.Column(db.Date)
    personCategory = db.Column(db.String(50))
    personCompany = db.Column(db.String(50))

    def __repr__(self):
        return f"{self.person}"
    # peopleEvents = db.Relationship("peopleEvents", backref="events", lazy="dynamic")

class exerciseTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id", name="fk_user_exercise"))
    day_id = db.Column(db.Integer, db.ForeignKey("day_table.id", name="fk_day_exercise"))
    exerciseDuration = db.Column(db.Integer)
    exerciseType = db.Column(db.String(50))
    exerciseDistance = db.Column(db.Float)

class ideaTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text)

class sourcesTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sourceTopic = db.Column(db.String(50))
    sourceLink = db.Column(db.String(200))
    sourceNote = db.Column(db.Text)

    
# class peopleEvents(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     place = db.Column(db.String(100))
#     date = db.Column(db.Date)
#     note = db.Column(db.Text)
#     user_id = db.Column(db.Integer, db.ForeignKey("user_table.id", name="fk_user_people"))
#     person_id = db.Column(db.Integer, db.ForeignKey("persons_table.id", name="fk_persons_event"))

#     def __repr__(self):
#         return f"{self.person} on {self.date}"
