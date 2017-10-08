from .. import db, models, app
from flask import flash, redirect, abort, render_template, url_for, request
from datetime import date as dt, time
from datetime import datetime
from .. import utils
from . import forms

empty_form = forms.EventForm.default_form()
empty_dateform = forms.DateForm.default_form()

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
        db.session.add(dateslot)

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
    event_dateslots = filter((lambda d : d.timeslots ), event_admin[0].dateslots)
    event_timeslots = reduce((lambda x,y : x + y), map((lambda x : x.timeslots), event_dateslots), [])
    event_times = map((lambda x : x.time), event_timeslots)
    event_dateslots_times = event_times

    participants = list(event.participants)

    form_type = forms.ParticipantForm.default_form(event_dateslots_times)
    form = form_type()

    return render_template('event_view.html', form=form, event=event, admin=event_admin, participants=participants, event_dateslots=event_dateslots, event_timeslots_times=event_dateslots_times)


@app.route("/event/<event_id>", methods=['POST'])
def show_event_post(event_id=None):
    """ POST - user adds participation """

    #Get event info
    event = get_event(event_id)
    admin_timeslots = event.admin.timeslots
    timeslot_times = [timeslot.time for timeslot in admin_timeslots]
    form_type = forms.ParticipantForm.default_form(timeslot_times)
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

@app.route("/event/<event_id>/new_dateslot", methods=['GET'])
def new_dateslot(event_id):
    return render_template('new_dateslot.html', form=empty_dateform())

@app.route("/event/<event_id>/new_dateslot", methods=['POST'])
def create_dateslot(event_id):

    event = get_event(event_id)
    form = empty_dateform(request.form)
    admin = event.admin

    if form.validate():

        dateslot = models.Dateslot(
            form.date.data,
            admin
        )
        db.session.add(dateslot)

        for timeslot in form.timeslots:
            val = form["slot_%s" % timeslot.strftime("%H%M")].data[0]
            if val is True:
                t = models.Timeslot(timeslot, dateslot)
                db.session.add(t)
        db.session.commit()

        return redirect(url_for("index"))
    else:
        return render_template("new_dateslot.html", form=form), 400
    

def get_event(id):
    """Utility function to get the first event matching id or None"""
    return models.Event.query.filter(models.Event.id == id).first()
