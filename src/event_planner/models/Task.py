import string
from .. import db
class Task(db.Model):
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
    The id of the `Participant` that this `Task` belongs to
    
    **Type:** INTEGER FOREIGN KEY
    """
    
    task = db.Column(db.Text)
    """
    The `datetime` that this `Timeslot` started at
    
    **Type:** TEXT
    """
    
    participant = db.relationship("Participant")
    """
    Relationship to the `Participant` that this `Task` belongs to
    
    **Related Model:** `event_planner.models.Participant`
    """
    
    def __init__(self, task, participant):
        """Creates a new `Timeslot` instance"""
        self.task = task
        self.participant = participant