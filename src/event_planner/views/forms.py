import datetime
from wtforms import Form, StringField, BooleanField, DateField, Field
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import HiddenInput
from .. import utils

class TimeslotInput(HiddenInput):
    """
    Widget for rendering a timeslot button
    """
    def __init__(self, timeslot):
        self._timeslot = timeslot
        super().__init__()
    def __call__(self, field, **kwargs):
        class_ = kwargs.pop("class_", "")
        val = field.data if field.data is not None else field.default
        val = "1" if val else "0"
        html = ["<div class=\"timeslot\">"]
        html.append("<p class=\"12-hour-form\">%s</p>" % self._timeslot.strftime("%I:%M %p"))
        html.append("<p class=\"24-hour-form\">%s</p>" % self._timeslot.strftime("%H:%M"))
        html.append("<input type=\"hidden\" class=\"%s\" value=\"%s\" name=\"%s\"/>" % (class_, val, field.name))
        html.append("</div>")
        return "\n".join(html)
class TimeslotField(BooleanField):
    def __init__(self, label="", validators=None, timeslot=datetime.time(), **kwargs):
        super().__init__(label, validators, default=False, **kwargs)
        self.widget = TimeslotInput(timeslot)
        self._timeslot = timeslot
    def process_formdata(self, value_list):
        self.data = [i == "1" for i in value_list]
    @property
    def timeslot(self):
        return self._timeslot
class EventForm(Form):
    """
    `Form` used for creating new `Event`s
    """
    eventname = StringField("eventname", [DataRequired()])
    eventdescription = StringField("eventdescription", [Optional()])
    adminname = StringField("adminname", [DataRequired()])
    date = DateField("date", [DataRequired()], format="%m/%d/%Y")
    @staticmethod
    def with_timeslots(timeslots=utils.all_timeslots()):
        """Returns `EventForm` as if it were declared with the given timeslots"""
        #TODO: Consider using interning since this is probably crazy slow
        ugly_type_suffix = "_".join([t.strftime("%H%M") for t in timeslots])
        #When copy.deepcopy() just won't do, simulate inheiritance and learn to love duck typing
        #This is needed because the copy module can't handle types...
        e = type("EventFormWith"+ugly_type_suffix, EventForm.__bases__, dict(EventForm.__dict__))
        for timeslot in timeslots:
            field_name = "slot_" + timeslot.strftime("%H%M")
            setattr(e, field_name, TimeslotField(field_name, [Optional()], timeslot=timeslot))
        e.timeslots = timeslots
        return e