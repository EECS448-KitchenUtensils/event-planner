from .. import db
class Timeslot(db.Model):
    """
    Database model for a `Participant`'s `Timeslot`s
    """
    id = db.Column(db.Integer, primary_key=True)
    """
    The primary key
    
    **Type:** INTEGER PRIMARY KEY
    """
    part_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    """
    The id of the `Participant` that this `Timeslot` belongs to
    
    **Type:** INTEGER FOREIGN KEY
    """
    datetime = db.Column(db.DateTime)
    """
    The `datetime` that this `Timeslot` started at
    
    **Type:** DATETIME
    """
    participant = db.relationship("Participant")
    """
    Relationship to the `Participant` that this `Timeslot` belongs to
    
    **Related Model:** `event_planner.models.Participant`
    """
    def __init__(self, datetime, participant):
        """Creates a new `Timeslot` instance"""
        self.datetime = datetime
        self.participant = participant