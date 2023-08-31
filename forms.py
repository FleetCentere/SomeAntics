from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, IntegerField, BooleanField, TextAreaField, FloatField, DateTimeField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, ValidationError
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
    dateMade = DateField("Date of Content Creation", validators=[DataRequired()])
    contentType = StringField("Type", validators=[DataRequired()])
    contentCreator = StringField("Creator", validators=[DataRequired()])
    contentLink = StringField("Link", validators=[DataRequired()])
    contentRating = IntegerField("Rating", validators=[DataRequired()])
    contentSubject = StringField("Subject", validators=[DataRequired()])
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
    exerciseDuration = IntegerField("Duration (min)")
    exerciseType = StringField("Type of Exercise")
    exerciseDistance = FloatField("Exericse Distance")
    submit = SubmitField("Add Event")

class ideasForm(FlaskForm):
    ideaNote = TextAreaField("Note", validators=[DataRequired()])
    submit = SubmitField("Add Note")