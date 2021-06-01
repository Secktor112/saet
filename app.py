from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_login import LoginManager



app = Flask(__name__)

app.config.from_object(Configuration)

db = SQLAlchemy(app)
manager = LoginManager(app)
