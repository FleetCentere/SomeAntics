from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "6c02a695213b2bb032979562d8177ba6"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
# db = SQLAlchemy(app)

from ProjectFiles import routes

# def nl2br(text):
#     return text.replace('\n', '<br>')
# app.jinja_env.filters['nl2br'] = nl2br