class TimeRange(object):
    """
    A holder for a range of time
    """
    def __init__(self, start, end):
        """Creates a new TimeRange instance"""
        self.start = start
        """The beginning time, usually a datetime.time"""
        self.end = end
        """The ending time, usually a datetime.time"""
