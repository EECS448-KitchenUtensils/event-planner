import string
import random
from .. import db
from . Participant import Participant
class Event(db.Model):
    """
    Database model for events
    
    Fields:
        * id: INTEGER PRIMARY KEY
        * title: TEXT
        * description: TEXT
        * date: DATE
        * admin_link: TEXT
    Relationships:
        * participants: 1 -> * Participant
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    admin_link = db.Column(db.Text)
    participants = db.relationship("Participant")
    def __init__(self, title, description, date, admin_name):
        """Creates a new Event instance"""
        self.title = title
        self.description = description
        self.date = date
        self.admin_link = "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(16)])
        self.admin_name = admin_name
