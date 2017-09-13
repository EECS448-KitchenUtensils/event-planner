from .. import db
from . EventParticipants import EventParticipants
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
    participants = db.relationship("EventParticipants",
        secondary=EventParticipants)
