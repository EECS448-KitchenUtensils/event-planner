from .. import db
class Timeslot(db.Model):
    """
    Database model for a `Dateslot`'s `Timeslot`s
    """

    id = db.Column(db.Integer, primary_key=True)
    """
    The primary key
    
    **Type:** INTEGER PRIMARY KEY
    """

    date_id = db.Column(db.Integer, db.ForeignKey("dateslot.id"))
    """
    The id of the `Dateslot` that this `Timeslot` belongs to
    
    **Type:** INTEGER FOREIGN KEY
    """

    time = db.Column(db.Time)
    """
    The `time` that this `Timeslot` started at
    
    **Type:** DATETIME
    """

    dateslot = db.relationship("Dateslot")
    """
    Relationship to the `Dateslot` that this `Timeslot` belongs to
    
    **Related Model:** `event_planner.models.Dateslot`
    """

    def __init__(self, time, dateslot):
        """Creates a new `Timeslot` instance"""
        self.time = time
        self.dateslot = dateslot