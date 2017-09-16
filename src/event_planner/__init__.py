from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from . import defaults
#Define the global flask app
app = Flask(__name__)
app.config.from_object(defaults)
app.config.from_envvar("EV_CONFIG")
#Insert stuff into the templating engine's world
from . import utils
app.jinja_env.globals.update(all_timeslots=utils.all_timeslots(),
    enumerate=enumerate)
#Start SQLAlchemy
db = SQLAlchemy(app)
#The imports come later so that the app and db objects are in existence
from . import models
from . import views

@app.cli.command("migrate")
def migrate_db():
    """Creates the database schema"""
    db.create_all()
@app.cli.command("purge-db")
def purge_db():
    """Purges the database"""
    db.drop_all()
    db.create_all()
#Static files here
# url_for('static', filename='style.css')
# url_for('static', filename='script.js')
# url_for('static', filename='toolkit-inverse.min.css')
# url_for('static', filename='toolkit.min.js')
