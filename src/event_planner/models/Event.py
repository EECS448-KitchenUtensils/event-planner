import string
import random
from .. import db
from . Participant import Participant
class Event(db.Model):
    """
    Database model for events
    """
    id = db.Column(db.Integer, primary_key=True)
    """Primary key (database detail)"""
    title = db.Column(db.Text)
    """Title of this event"""
    description = db.Column(db.Text)
    """Description of this event"""
    date = db.Column(db.Date)
    """Date of this event"""
    admin_link = db.Column(db.Text)
    """Magic admin code for this event"""
    admin_name = db.Column(db.Text)
    """ Name of admin """
    participants = db.relationship("Participant")
    def __init__(self, title, description, date, admin_name):
        """Creates a new Event instance"""
        self.title = title
        self.description = description
        self.date = date
        self.admin_link = "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(16)])
        self.admin_name = admin_name
