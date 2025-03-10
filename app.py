from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_migrate as fm

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///candidates.db"

db.init_app(app)

migrate = fm.Migrate(app, db)

from routes.candidates import *
from routes.about import *

if(__name__ == '__main__'):
    app.run()
    