from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired


class pressReleaseForm(FlaskForm):
    contentDate = DateField("Date of Content Creation", validators=[DataRequired()])
    company = StringField("Company Name", validators=[DataRequired()])
    ticker = StringField("Company Ticker", default="na")
    link = StringField("Press Release Link", validators=[DataRequired()])
    submit = SubmitField("Submit")
