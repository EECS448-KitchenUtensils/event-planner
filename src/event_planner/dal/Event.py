class Event(object):
    """
    Represents an event instance
    """
    def __init__(self):
        self.admin_link = ""
        """The magic string used to authenicate a admin user"""
        self.id = ""
        """The id of the event (UUID)"""
        self.time_slots = []
        """A list of TimeRange of the timeslots for this event"""
        self.participants = []
        """A list of Participants for this event"""
