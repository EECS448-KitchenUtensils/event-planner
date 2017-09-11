class Participant(object):
    """
    An event participant
    """
    def __init__(self):
        """
        Creates a Participant Event
        """
        self.time_slots = []
        """The TimeRange objects representing the availablity of this participant"""
        self.name = ""
        """The name of this partipant"""
