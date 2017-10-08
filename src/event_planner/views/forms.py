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
        super(TimeslotInput, self).__init__()

    def __call__(self, field, **kwargs):
        class_ = kwargs.pop("class_", "")
        val = field.data[0] if hasattr(field.data, "__len__") else field.default

        html = ["<div id=\"slot_button_%s\" class=\"timeslot\">" % field._timeslot.strftime("%H%M")]
        html.append("<p class=\"12-hour-form\">%s</p>" % self._timeslot.strftime("%I:%M %p"))
        html.append("<p class=\"24-hour-form\">%s</p>" % self._timeslot.strftime("%H:%M"))
        html.append("<input type=\"hidden\" class=\"%s\" value=\"%s\" name=\"%s\"/>" % (class_, ("1" if val else "0"), field.name))
        html.append("</div>")

        if val is True:
            #jQuery UI selectable workaround
            html.append("<script> $(document).ready(function() {$(\"#slot_button_%s\").removeClass(\"ui-selected\").addClass(\"ui-selected\").addClass(\"active\");});</script>" % self._timeslot.strftime("%H%M"))

        return "\n".join(html)

class TimeslotField(BooleanField):
    def __init__(self, label="", validators=None, timeslot=datetime.time(), **kwargs):
        super(TimeslotField, self).__init__(label, validators, default=False, **kwargs)
        self.widget = TimeslotInput(timeslot)
        self._timeslot = timeslot
    def process_formdata(self, value_list):
        self.data = [i == "1" for i in value_list]
    @property
    def timeslot(self):
        return self._timeslot

def with_timeslots(form_type, timeslots):
    """Returns `EventForm` as if it were declared with the given timeslots"""
    #TODO: Consider using interning since this is probably crazy slow
    ugly_type_suffix = "_".join([t.strftime("%H%M") for t in timeslots])

    #When copy.deepcopy() just won't do, simulate inheiritance and learn to love duck typing
    #This is needed because the copy module can't handle types...
    fresh_type = type(form_type.__name__+"With"+ugly_type_suffix, form_type.__bases__, dict(form_type.__dict__))

    for timeslot in timeslots:
        field_name = "slot_" + timeslot.strftime("%H%M")
        setattr(fresh_type, field_name, TimeslotField(field_name, [Optional()], timeslot=timeslot))
    fresh_type.timeslots = timeslots

    return fresh_type

class EventForm(Form):
    """
    `Form` used for creating new `Event`s
    """
    eventname = StringField("eventname", [DataRequired(message='Event Name cannot be empty')])
    eventdescription = StringField("eventdescription", [Optional()])
    adminname = StringField("adminname", [DataRequired(message='Admin Name cannot be empty')])
    date = DateField("date", [DataRequired('Date is empty or invalid')], format="%m/%d/%Y")

    @staticmethod
    def default_form(timeslots=utils.all_timeslots()):
        return with_timeslots(EventForm, timeslots)

class ParticipantForm(Form):
    """
    `Form` used for creating new `Participant`s
    """
    participantname = StringField("participantname", [DataRequired(message='Participant Name cannot be empty')])

    @staticmethod
    def default_form(timeslots=utils.all_timeslots()):
        return with_timeslots(ParticipantForm, timeslots)

class DateForm(Form):
    """
    `Form` used for creating new `Date`s
    """
    date = DateField("date", [DataRequired('Date is empty or invalid')], format="%m/%d/%Y")

    @staticmethod
    def default_form(timeslots=utils.all_timeslots()):
        return with_timeslots(DateForm, timeslots)
