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

    return render_template('event_view.html', event=event, admin=event_admin, participants=participants, event_timeslots=event_timeslots, event_timeslots_times=event_timeslots_times)


@app.route("/event/<event_id>", methods=['POST'])
def show_event_post(event_id=None):
    """ POST - user adds participation """

    #Get event info
    event = get_event(event_id)

    error = False

    slotdata = []
    slotdata_error_flag = False
    for x in range(0,47):
        if request.form['slot_%s' % x] != 0 or request.form['slot_%s' % x] != 1:
            slotdata_error_flag == True
        slotdata.append(request.form['slot_%s' % x])
    if slotdata_error_flag:
        error = True
        flash('Internal parsing error (Timeslot form elements corrupt)')

    name = request.form["participantname"]
    if name == "" or name.isspace():
        error = True
        flash("The participant's name is empty.")
        
    if not error:

        #Get Database models ready
        #Add the participant
        new_participant = models.Participant(name, event, False)
        db.session.add(new_participant)
        #input_list_to_time_list is a function from utils.py
        times_list = utils.input_list_to_time_list(slotdata)
        for t in times_list:
            db.session.add(models.Timeslot(t, new_participant))


        db.session.commit()

    return redirect(url_for('show_event_get', event_id=event_id))

def get_event(id):
    """Utility function to get the first event matching id or None"""
    return models.Event.query.filter(models.Event.id == id).first()
