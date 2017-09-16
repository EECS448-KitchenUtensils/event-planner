from datetime import time

def input_list_to_time_list(input_list):
    """Converts a list of inputs from a form into a list of datetime.time objects"""
    time_list = []
    for x,input in enumerate(input_list):
        if input != 0 and input != '0':
            time_24 = x // 2
            minutes = 0
            if x % 2 == 1:
                minutes = 30
            time_list.append(time(hour=time_24, minute=minutes))
    return time_list

def all_timeslots():
    """Returns a list of datetime.time objects for every 30 minute interval"""
    return [time(i//2, (i%2)*30) for i in range(48)]

class FieldParser(object):
    """Helper object to parse the fields in a flask request.form object"""
    class ParsedField(object):
        """
        Voldemort object to return value
        
        Properties
        ----------
        field : str
            The field that this instance represents
        value : str
            The value of this field
        """
        def __init__(self, name, value):
            self._name = name
            self._value = value
        def __repr__(self):
            return "<name=%s, value=%s>" % (self._name, self._value)
        @property
        def field(self):
            """The name of this field"""
            return self._name
        @property
        def value(self):
            """The value of this field, cannot be None"""
            return self._value
    def __init__(self, req, allow_empty):
        """
        Creates a new instance of FieldParser

        Parameters
        ----------
        req : dict
            The Flask request.form object
        allow_empty: bool
            Whether empty string should be allowed or saturated to None
        """
        self._req = req
        self._allow_empty = allow_empty
    def parse(self, field_name):
        """Parses out a given field name without throwing exceptions"""
        val = request.form.get(field_name)
        is_empty = val is not None and val == "" or val.isspace()
        if val or (self._allow_empty and is_empty):
            return ParsedField(field_name, val)
        else:
            return None
    @property
    def allow_empty(self):
        """True if empty or whitespace strings are allowed, False otherwise"""
        return self._allow_empty