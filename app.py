from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///candidates.db"

db.init_app(app)

from routes import *

if(__name__ == '__main__'):
    app.run()
    