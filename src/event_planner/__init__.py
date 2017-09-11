from flask import Flask, render_template, url_for

#Define the global flask app
app = Flask(__name__)

from . import models
from . import views

#Static files here
# url_for('static', filename='style.css')
# url_for('static', filename='script.js')
# url_for('static', filename='toolkit-inverse.min.css')
# url_for('static', filename='toolkit.min.js')