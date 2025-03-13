from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_migrate as fm
from dotenv import load_dotenv
import os

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///candidates.db"

load_dotenv()

db.init_app(app)

migrate = fm.Migrate(app, db)

from routes.candidates import *
from routes.about import *
from routes.authenticantion  import *

if(__name__ == '__main__'):
    app.run()
    