from .. import db
class Timeslot(db.Model):
    """Model to allow a participant to have multiple timeslots"""
    id = db.Column(db.Integer, primary_key=True)
    """Primary key"""
    part_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    """The id of the Participant model that this Timeslot belongs to"""
    time = db.Column(db.Time)
    """The time that this timeslot started at"""
    participant = db.relationship("Participant")
    def __init__(self, time, participant):
        self.time = time
        self.participant = participant
