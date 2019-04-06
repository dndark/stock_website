
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)

# enable CORS
CORS(app)
# app.config.from_object(__name__)

app.config.from_object(config["default"])
# app.config.from_object(config["ItemStorage"])
SQLAlchemy
db = SQLAlchemy(app)

from app import models,views