from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, IntegerField, BooleanField, TextAreaField
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

class newTaskForm(FlaskForm):
    taskCategory = StringField("Category", validators=[DataRequired()])
    taskName = StringField("Name", validators=[DataRequired()])
    taskLink = StringField("Link")
    taskNote = TextAreaField("Note")
    submit = SubmitField("Add Task")

# class pressReleaseForm(FlaskForm):
#     contentDate = DateField("Date of Content Creation", validators=[DataRequired()])
#     company = StringField("Company Name", validators=[DataRequired()])
#     ticker = StringField("Company Ticker", default="na")
#     link = StringField("Link", validators=[DataRequired()])
#     product = StringField("Content Product", validators=[DataRequired()])
#     submit = SubmitField("Submit")

# class ideaForm(FlaskForm):
#     category = StringField("Category", validators=[DataRequired()])
#     link = StringField("Link", validators=[DataRequired()])
#     note = StringField("Note", validators=[DataRequired()])
#     status = StringField("Status")
#     submit = SubmitField("Submit")

# class contentForm(FlaskForm):
#     dateMade = DateField("Date of Content Creation", validators=[DataRequired()])
#     contentType = StringField("Type of Content", validators=[DataRequired()])
#     contentCreator = StringField("Content Creator", validators=[DataRequired()])
#     contentLink = StringField("Link")
#     contentNote = StringField("Note about content")
#     contentRating = IntegerField("Rating of content")
#     submit = SubmitField("Submit")

# class companyForm(FlaskForm):
#     ticker = StringField("Company Ticker", validators=[DataRequired()])
#     startYear = IntegerField("Start Year", validators=[DataRequired(), NumberRange(2018, 2023)])
#     holderCount = IntegerField("Number of Holders", validators=[DataRequired(), NumberRange(1, 100)])
#     submit = SubmitField("Submit")
