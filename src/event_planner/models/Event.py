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
    participants = db.relationship("Participant")
    def __init__(self, title, description, date):
        """Creates a new Event instance"""
        self.title = title
        self.description = description
        self.date = date
        self.admin_link = "foo"
