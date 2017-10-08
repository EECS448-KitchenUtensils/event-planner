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

    @property
    def admin(self):
        #TODO: Make this a query, not a for loop
        for participant in self.participants:
            if participant.is_admin:
                return participant
                
    def __init__(self, title, description):
        """
        Creates a new `Event` instance
        """
        self.title = title
        self.description = description
        self.admin_link = "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(16)])
