from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from ProjectFiles.api_keys import secret_key


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or \
     'sqlite:///' + os.path.join(basedir, 'app.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)

login = LoginManager(app)
login.login_view = "login"

from ProjectFiles import routes, models

# def nl2br(text):
#     return text.replace('\n', '<br>')
# app.jinja_env.filters['nl2br'] = nl2br