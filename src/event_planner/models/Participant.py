from .. import db
class Participant(db.Model):
    """
    Database model for participants
    """
    id = db.Column(db.Integer, primary_key=True)
    """
    The primary key for the database

    **Type:** INTEGER PRIMARY KEY
    """
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    """
    The key of the `Event` that this `Participant` belongs to

    **Type:** INTEGER FOREIGN KEY
    """
    event = db.relationship("Event")
    """
    The `Event` that this `Participant` belongs to

    **Related Model:** `event_planner.models.Event`
    """
    name = db.Column(db.Text)
    """
    The name of this `Participant`

    **Type:** TEXT
    """
    timeslots = db.relationship("Timeslot")
    """
    The `Timeslot`s that belong to this `Participant`

    **Related Models:** `event_planner.models.Timeslot`
    """
    tasks = db.relationship("Task")
    """
    The `Task`s that belong to this `Participant`

    **Related Models:** `event_planner.models.Task`
    """
    is_admin = db.Column(db.Boolean)
    """
    Whether or not this `Participant` is an admin for its `Event`

    **Type:** BOOLEAN
    """
    def __init__(self, name, event, is_admin):
        """
        Creates a new `Participant` instance
        """
        self.name = name
        self.event = event
        self.is_admin = is_admin
