from .. import db
from . TimeslotEnum import TimeslotEnum
class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    timeslot = db.Column(db.Enum(TimeslotEnum))
