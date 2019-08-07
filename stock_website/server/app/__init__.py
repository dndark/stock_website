
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

from . import main
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app = Flask(__name__,template_folder="templates",static_folder="static",static_url_path="/server/app/static")

# enable CORS
CORS(app)
# app.config.from_object(__name__)

app.config.from_object(config["default"])
app.register_blueprint(main.main)
app.register_blueprint(api.api)
# app.config.from_object(config["ItemStorage"])
# SQLAlchemy
db = SQLAlchemy(app)
# db2019 = SQLAlchemy(app)

# 2018
db2018 = SQLAlchemy(app)
db2017 = SQLAlchemy(app)
from app import models,views