from .. import db

EventParticipants = db.Table("EventParticipants",
    db.Column("event_id", db.Integer, db.ForeignKey("Event.id")),
    db.Column("participant_id", db.Integer, db.ForeignKey("Participant.id"))
)
