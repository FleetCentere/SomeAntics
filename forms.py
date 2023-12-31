from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, IntegerField, BooleanField, TextAreaField, FloatField, DateTimeField, DecimalField, TimeField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, ValidationError, Optional
from ProjectFiles.models import userTable

class loginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = userTable.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username")

    def validate_email(self, email):
        user = userTable.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address")

class editProfileForm(FlaskForm):
    password_check = PasswordField("Confirm Prior Password")
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class newTaskForm(FlaskForm):
    taskCategory = StringField("Category", validators=[DataRequired()])
    taskName = StringField("Name", validators=[DataRequired()])
    taskLink = StringField("Link")
    taskNote = TextAreaField("Note")
    submit = SubmitField("Add Task")

class newContentForm(FlaskForm):
    contentComplete = BooleanField("Complete")
    dateConsumed = DateField("Date of Addition", validators=[DataRequired()])
    dateMade = DateField("Date of Content Creation", validators=[DataRequired()])
    contentCreator = StringField("Creator")
    contentLink = StringField("Link")
    contentRating = IntegerField("Rating")
    contentSubject = StringField("Subject")
    contentNote = TextAreaField("Note")
    contentTitle = StringField("Title")
    contentType = SelectField("Type", choices=[])
    submit = SubmitField("Add Content")

class newNewsForm(FlaskForm):
    newsType = StringField("Type", validators=[DataRequired()])
    newsTitle = StringField("Title", validators=[DataRequired()])
    newsNote = TextAreaField("Note")
    newsLink = StringField("Link", validators=[DataRequired()])
    newsTicker = StringField("Ticker")
    newsDatePosted = DateField("News Date", validators=[DataRequired()])
    submit = SubmitField("Add News")

class newEventForm(FlaskForm):
    eventType = StringField("Type", validators=[DataRequired()])
    eventDate = DateField("Event Date")
    eventTime = TimeField("Event Time")
    eventLocation = StringField("Location")
    eventNote = TextAreaField("Note")
    eventPeople = SelectMultipleField("People at event", choices=[], coerce=int)
    submit = SubmitField("Add Event")

class newExerciseForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    exerciseType = StringField("Type of Exercise", validators=[Optional()])
    exerciseDuration = IntegerField("Duration (min)")
    exerciseDistance = FloatField("Exericse Distance")
    submit = SubmitField("Add Exercise")

class dailyForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    sleep = StringField("Sleep Location")
    morning = TextAreaField("Morning")
    afternoon = TextAreaField("Afternoon")
    evening = TextAreaField("Evening")
    weight = DecimalField("Weight (lbs)", validators=[Optional()])
    journal = TextAreaField("Evening")
    submitPersonal = SubmitField("Submit Personal")
    submitContent = SubmitField("Submit Content")

class ideasForm(FlaskForm):
    ideaNote = TextAreaField("Note", validators=[DataRequired()])
    submit = SubmitField("Idea Note")

class sourcesForm(FlaskForm):
    sourceTopic = StringField("Source Topic")
    sourceLink = StringField("Source Link")
    sourceNote = TextAreaField("Source Note")
    submit = SubmitField("Submit Source")

class companyForm(FlaskForm):
    ticker = StringField("Ticker")
    startYear = IntegerField("Start Year")
    holderCount = IntegerField("Number of Holders")
    submit = SubmitField("Submit")

class personForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    background = TextAreaField("Background")
    birthday = DateField("Birthday", validators=[Optional()])
    category = StringField("Category", validators=[DataRequired()])
    company = StringField("Company")
    submit = SubmitField("Submit")

class listForm(FlaskForm):
    ticker = StringField("Ticker", validators=[DataRequired()])
    submit = SubmitField("Submit")

class computerScienceForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    link = StringField("Link")
    priority = IntegerField("Priority")
    submit = SubmitField("Submit")

class computerSciencePosts(FlaskForm):
    title = StringField("Title") 
    note = TextAreaField("Note")
    submit = SubmitField("Submit")

class jobForm(FlaskForm):
    job = StringField("Job") 
    contact = StringField("Contact")
    status = TextAreaField("Status")
    probability = IntegerField("Probability")
    submit = SubmitField("Submit")

class financeForm(FlaskForm):
    title = StringField("Title")
    link = StringField("Link")
    product = StringField("Product")
    size = IntegerField("Size")
    ticker = StringField("Ticker")
    note = TextAreaField("Note")
    date = DateField("Date")
    submit = SubmitField("Submit")

class postForm(FlaskForm):
    title = StringField("Title")
    note = TextAreaField("Note")
    submit = SubmitField("Submit")

class thoughtForm(FlaskForm):
    thought = TextAreaField("Thought")
    submit = SubmitField("Submit")

class sourcesForm(FlaskForm):
    source = StringField("Source")
    author = StringField("Author")
    submit = SubmitField("Submit")