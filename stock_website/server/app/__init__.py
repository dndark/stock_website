
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
# db2019 = SQLAlchemy(app)

# 2018
db2018 = SQLAlchemy(app)
db2017 = SQLAlchemy(app)
from app import models,views