from .. import db
class Timeslot(db.Model):
    """
    Database model for a Participant's timeslots
    Fields:
        * id: INTEGER PRIMARY KEY
        * part_id: INTEGER FOREIGN KEY
        * time: TIME
    Relationships:
        * participant: The parent Participant for this Timeslot
    """
    id = db.Column(db.Integer, primary_key=True)
    """Primary key"""
    part_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    """The id of the Participant model that this Timeslot belongs to"""
    time = db.Column(db.Time)
    """The time that this timeslot started at"""
    participant = db.relationship("Participant")
    """Relationship to the participant model"""
    def __init__(self, time, participant):
        self.time = time
        self.participant = participant
        
