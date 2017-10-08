from .. import db
class Dateslot(db.Model):
    """
    Database model for a `Participant`'s `Dateslot`s
    """

    id = db.Column(db.Integer, primary_key=True)
    """
    The primary key
    
    **Type:** INTEGER PRIMARY KEY
    """

    part_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    """
    The id of the `Participant` that this `Dateslot` belongs to
    
    **Type:** INTEGER FOREIGN KEY
    """

    date = db.Column(db.Date)
    """
    The `date` that this `Dateslot` started at
    
    **Type:** DATETIME
    """

    participant = db.relationship("Participant")
    """
    Relationship to the `Participant` that this `Dateslot` belongs to
    
    **Related Model:** `event_planner.models.Participant`
    """

    timeslots = db.relationship("Timeslot")
    """
    The `Timeslot`s that belong to this `Participant`

    **Related Models:** `event_planner.models.Timeslot`
    """
    
    def __init__(self, date, participant):
        """Creates a new `Dateslot` instance"""
        self.date = date
        self.participant = participant