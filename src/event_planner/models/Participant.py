from .. import db
class Participant(db.Model):
    """
    Database model for participants

    Fields:
        * id: INTEGER PRIMARY KEY
        * event_id: INTEGER FOREIGN KEY
        * name: TEXT
        * is_admin: BOOLEAN
    Relationships:
        * event: Parent Event for this Participant
        * timeslots: 1 -> * Timeslots for this Participant
    """
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    event = db.relationship("Event")
    name = db.Column(db.Text)
    timeslots = db.relationship("Timeslot")
    is_admin = db.Column(db.Boolean)
    def __init__(self, name, event, is_admin):
        self.name = name
        self.event = event
        self.is_admin = is_admin
