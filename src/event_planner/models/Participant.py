from .. import db
class Participant(db.Model):
    """
    Database model for participants
    """
    id = db.Column(db.Integer, primary_key=True)
    """Database primary key"""
    name = db.Column(db.Text)
    """Name of this event"""
    timeslots = db.relationship("ParticipantTimeslots")
    """Timeslots that this participant is available"""
