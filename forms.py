from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class pressReleaseForm(FlaskForm):
    contentDate = DateField("Date of Content Creation", validators=[DataRequired()])
    company = StringField("Company Name", validators=[DataRequired()])
    ticker = StringField("Company Ticker", default="na")
    link = StringField("Link", validators=[DataRequired()])
    product = StringField("Content Product", validators=[DataRequired()])
    submit = SubmitField("Submit")

class companyForm(FlaskForm):
    ticker = StringField("Company Ticker", validators=[DataRequired()])
    startYear = IntegerField("Start Year", validators=[DataRequired(), NumberRange(2018, 2023)])
    holderCount = IntegerField("Number of Holders", validators=[DataRequired(), NumberRange(1, 100)])
    submit = SubmitField("Submit")
