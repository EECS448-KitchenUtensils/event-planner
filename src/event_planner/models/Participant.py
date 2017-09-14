from .. import db
class Participant(db.Model):
    """
    Database model for participants
    """
    id = db.Column(db.Integer, primary_key=True)
    """Database primary key"""
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    """Foreign key back to the parent event"""
    event = db.relationship("Event")
    """Parent event"""
    name = db.Column(db.Text)
    """Name of this event"""
    timeslots = db.relationship("Timeslot")
    """Timeslots that this participant is available"""
    def __init__(self, name, event):
        self.name = name
        self.event = event
