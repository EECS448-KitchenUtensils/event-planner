from flask import Flask

#Define the global flask app
app = Flask(__name__)

from . import models
from . import views
