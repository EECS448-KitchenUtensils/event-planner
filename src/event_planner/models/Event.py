import string
import random
from .. import db
from . Participant import Participant
class Event(db.Model):
    """
    Database model for events
    """
    id = db.Column(db.Integer, primary_key=True)
    """
    The primary key for the database
    
    **Type:** INTEGER PRIMARY KEY
    """
    title = db.Column(db.Text)
    """
    The title of this event

    **Type:** TEXT
    """
    description = db.Column(db.Text)
    """
    The description of this event

    **Type:** TEXT
    """
    date = db.Column(db.Date)
    """
    The date that this event takes place on

    **Type:** DATE
    """
    admin_link = db.Column(db.Text)
    """
    The *magic* code that authenicates the admin for this event

    **Type:** TEXT
    """
    participants = db.relationship("Participant")
    """
    Relationship to the participants of this event

    **Related Model:** `event_planner.models.Participant`
    """
    def __init__(self, title, description, date):
        """
        Creates a new `Event` instance
        """
        self.title = title
        self.description = description
        self.date = date
        self.admin_link = "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(16)])
