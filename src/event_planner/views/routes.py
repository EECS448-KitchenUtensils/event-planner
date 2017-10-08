from .. import db, models, app
from flask import flash, redirect, abort, render_template, url_for, request
from datetime import date as dt, time
from datetime import datetime
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
            form.eventdescription.data
        )
        db.session.add(event)

        admin = models.Participant(
            form.adminname.data,
            event,
            True
        )
        db.session.add(admin)

        dateslot = models.Dateslot(
            form.date.data,
            admin
        )

        for timeslot in form.timeslots:
            val = form["slot_%s" % timeslot.strftime("%H%M")].data[0]
            if val is True:
                t = models.Timeslot(timeslot, dateslot)
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
    event_dateslots = event_admin[0].dateslots
    event_dateslots_times = []

    for dateslot in event_dateslots
        for timeslot in dateslot:
            event_dateslots_times.append(timeslot.time)

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

    return redirect(url_for('show_event_get', event_id=event_id))

def get_event(id):
    """Utility function to get the first event matching id or None"""
    return models.Event.query.filter(models.Event.id == id).first()
