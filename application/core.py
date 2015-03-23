from application import app

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from application.sessions import ItsdangerousSessionInterface as session_interface

db = SQLAlchemy(app)

api_manager = APIManager(app, flask_sqlalchemy_db=db)

app.session_interface = session_interface()