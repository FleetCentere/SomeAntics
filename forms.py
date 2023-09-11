from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, IntegerField, BooleanField, TextAreaField, FloatField, DateTimeField
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
    contentType = StringField("Type", validators=[DataRequired()])
    contentCreator = StringField("Creator")
    contentLink = StringField("Link")
    contentRating = IntegerField("Rating")
    contentSubject = StringField("Subject")
    contentNote = TextAreaField("Note")
    submit = SubmitField("Add Content")

class newNewsForm(FlaskForm):
    newsType = StringField("Type", validators=[DataRequired()])
    newsTitle = StringField("Title", validators=[DataRequired()])
    newsNote = TextAreaField("Note")
    newsLink = StringField("Link", validators=[DataRequired()])
    newsTicker = StringField("Ticker", validators=[DataRequired()])
    newsDatePosted = DateField("Date of Event", validators=[DataRequired()])
    submit = SubmitField("Add News")

class newEventForm(FlaskForm):
    eventType = StringField("Type", validators=[DataRequired()])
    eventDatetime = DateTimeField("Event Date and Time")
    eventLocation = StringField("Location", validators=[DataRequired()])
    eventNote = TextAreaField("Note", validators=[DataRequired()])
    submit = SubmitField("Add Event")

class newExerciseForm(FlaskForm):
    exerciseDate = DateField("Date", validators=[DataRequired()])
    exerciseType = StringField("Type of Exercise", validators=[Optional()])
    exerciseDuration = IntegerField("Duration (min)")
    exerciseDistance = FloatField("Exericse Distance")
    submit = SubmitField("Add Exercise")

class ideasForm(FlaskForm):
    ideaNote = TextAreaField("Note", validators=[DataRequired()])
    submit = SubmitField("Idea Note")

class dailyForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    sleep = StringField("Sleep Location")
    morning = TextAreaField("Morning")
    afternoon = TextAreaField("Afternoon")
    evening = TextAreaField("Evening")
    weight = FloatField("Weight (lbs)")
    journal = TextAreaField("Evening")
    submitPersonal = SubmitField("Submit Personal")
    submitContent = SubmitField("Submit Content")