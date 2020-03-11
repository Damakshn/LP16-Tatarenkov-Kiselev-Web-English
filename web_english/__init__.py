from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object("web_english.config.DevConfig")
db = SQLAlchemy(app)

import web_english.models
import web_english.views
