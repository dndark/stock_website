
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
app.url_map.strict_slashes = False

# enable CORS
CORS(app)

app.config.from_object(config["default"])
app.register_blueprint(main.main)
# app.config.from_object(config["ItemStorage"])
# SQLAlchemy
db = SQLAlchemy(app)
# db2019 = SQLAlchemy(app)
db2018 = SQLAlchemy(app)
db2017 = SQLAlchemy(app)
from app import models,views