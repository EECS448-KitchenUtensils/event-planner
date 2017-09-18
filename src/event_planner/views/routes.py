from .. import db, models, app
from flask import flash, redirect, abort, render_template, url_for, request
from datetime import date as dt, time
from .. import utils
from . import forms

empty_form = forms.EventForm.with_timeslots()

@app.route("/")
def index():
    """GET - Default view of all events"""
    events = models.Event.query.all()

    return render_template('index.html', events=events)

@app.route("/new", methods=['GET'])
def new_get():
    """GET - New event form"""
    return render_template('new.html', form=empty_form())

@app.route("/new", methods=['POST'])
def new_post():
    """Creates a new event and commits it to the db"""

    form = empty_form(request.form)
    if form.validate():
        event = models.Event(
            form.eventname.data,
            form.eventdescription.data,
            form.date.data
        )
        db.session.add(event)
        admin = models.Participant(
            form.adminname.data,
            event,
            True
        )
        db.session.add(admin)
        for timeslot in form.timeslots:
            val = form["slot_%s" % timeslot.strftime("%H%M")].data[0]
            if val is True:
                t = models.Timeslot(timeslot, admin)
                db.session.add(t)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("new.html", form=form), 400

@app.route("/event/<event_id>", methods=['GET'])
def show_event_get(event_id):
    """ GET - user view of event"""

    #Get event by ID from DB and send to event view
    event = get_event(event_id) or abort(404) 
    event_admin = list(filter(lambda x: x.is_admin == True, event.participants))
    event_timeslots = event_admin[0].timeslots
    event_timeslots_times = []
    for t in event_timeslots:
        event_timeslots_times.append(t.time)

    participants = list(event.participants)

    form_type = forms.ParticipantForm.with_timeslots(event_timeslots_times)
    form = form_type()
    return render_template('event_view.html', form=form, event=event, admin=event_admin, participants=participants, event_timeslots=event_timeslots, event_timeslots_times=event_timeslots_times)


@app.route("/event/<event_id>", methods=['POST'])
def show_event_post(event_id=None):
    """ POST - user adds participation """

    #Get event info
    event = get_event(event_id)
    admin_timeslots = event.admin.timeslots
    timeslot_times = [timeslot.time for timeslot in admin_timeslots]
    form_type = forms.ParticipantForm.with_timeslots(timeslot_times)
    form = form_type(request.form)
    if form.validate():
        participant = models.Participant(form.participantname.data, event, False)
        db.session.add(participant)
        for slot in form.timeslots:
             val = form["slot_%s" % slot.strftime("%H%M")].data[0]
             if val is True:
                t = models.Timeslot(slot, participant)
                db.session.add(t)
        db.session.commit()
<<<<<<< HEAD

    return redirect(url_for('show_event_get', event_id=event_id))
=======
        return redirect(url_for('show_event_get', event_id=event_id))
    return render_template("event_view.html",
        event=event,
        admin=event.admin,
        participants=list(event.participants),
        event_timeslots=admin_timeslots,
        event_timeslot_times=list(map(lambda timeslot: timeslot.time, admin_timeslots)),
        form=form), 400
@app.route("/event/<event_id>/<event_auth_token>", methods=['GET'])
def show_event_get_admin(event_id=None, event_auth_token=None):
    """ GET - admin view """
    #Get event by ID from DB and send to event view
    event = get_event(event_id)


    #Create the dates to show in the template for iterator.
    daterange = ['12:00 AM', '12:30 AM', '1:00 AM', '1:30 AM', '2:00 AM', '2:30 AM','3:00 AM', '3:30 AM', '4:00 AM', '4:30 AM', '5:00 AM', '5:30 AM', '6:00 AM', '6:30 AM', '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM', '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM']
    daterange24 = ['0:00', '0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
    daterange = enumerate(daterange)

    return render_template('event_manage.html', event=event, event_auth_token=event_auth_token, daterange=daterange, daterange24=daterange24)

@app.route("/event/<event_id>/<event_auth_token>", methods=['POST'])
def show_event_post_admin(event_id=None, event_auth_token=None):
    """ POST - admin changes """
    # TODO pull in all data about the event and put in the database

    #Get event by ID from DB and send to event view
    event = get_event(event_id)

    #Create the dates to show in the template for iterator.
    daterange = ['12:00 AM', '12:30 AM', '1:00 AM', '1:30 AM', '2:00 AM', '2:30 AM','3:00 AM', '3:30 AM', '4:00 AM', '4:30 AM', '5:00 AM', '5:30 AM', '6:00 AM', '6:30 AM', '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM', '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM']
    daterange24 = ['0:00', '0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
    daterange = enumerate(daterange)

    return render_template('event_manage.html', event=event, event_auth_token=event_auth_token, daterange=daterange, daterange24=daterange24)
>>>>>>> cecf1649f1a965c4d7d5c13cef616916e2481ea6

def get_event(id):
    """Utility function to get the first event matching id or None"""
    return models.Event.query.filter(models.Event.id == id).first()
