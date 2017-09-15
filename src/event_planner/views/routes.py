from .. import db, models, app, render_template, url_for, request
from flask import flash, redirect
from datetime import date as dt, time
from .. import utils

@app.route("/")
def index():

    events = models.Event.query.all()

    return render_template('index.html', events=events)

@app.route("/new", methods=['GET'])
def new_get():
    return render_template('new.html', timeslots=[time(i//2, (i%2)*30) for i in range(48)])

@app.route("/new", methods=['POST'])
def new_post():
    """Creates a new event and commits it to the db"""
    error = False

    #Check basic for elements (Besides time slot)
    name = request.form['eventname']
    if name == "" or name.isspace():
        error = True
        flash("The event name is empty.")

    desc = request.form['eventdescription']

    admin = request.form['adminname']
    if admin == "" or name.isspace():
        error = True
        flash("The admin's name is required")

    try:
        month, day, year = request.form['date'].split('/')
        event_date = dt(int(year), int(month), int(day))
    except:
        error = True
        flash('Date empty or format error')

    #Parse and check timeslot elements
    slotdata_error_flag = False
    slotdata = []
    for x in range(0,47):
        if request.form['slot_%s' % x] != 0 or request.form['slot_%s' % x] != 1:
            slotdata_error_flag == True
        slotdata.append(request.form['slot_%s' % x])
    if slotdata_error_flag:
        error = True
        flash('Internal parsing error (Timeslot form elements corrupt)')

    #Commit to db if no error.
    if not error:

        #Create each model, references go in constructors

        event = models.Event(name, desc, event_date, admin)
        db.session.add(event)

        admin_model = models.Participant(admin, event, True)
        db.session.add(admin_model)

        #input_list_to_time_list is a function from utils.py
        times_list = utils.input_list_to_time_list(slotdata)
        for t in times_list:
            db.session.add(models.Timeslot(t, admin_model))


        db.session.commit()

    return redirect(url_for('new_get'))

@app.route("/event/<event_id>", methods=['GET'])
def show_event_get(event_id):
    """ GET - user view of event"""

    #Get event by ID from DB and send to event view
    event = get_event(event_id)
    event_admin = list(filter(lambda x: x.is_admin == True, event.participants))
    event_timeslots = event_admin[0].timeslots

    

    participants = list(event.participants)

    return render_template('event_view.html', event=event, admin=event_admin, participants=participants, event_timeslots=event_timeslots)


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

@app.route("/event/<event_id>/<event_auth_token>", methods=['GET'])
def show_event_get_admin(event_id=None, event_auth_token=None):
    """ GET - admin view """
    #Get event by ID from DB and send to event view
    event = get_event(event_id)
    return render_template('event_manage.html', event=event, event_auth_token=event_auth_token)

@app.route("/event/<event_id>/<event_auth_token>", methods=['POST'])
def show_event_post_admin(event_id=None, event_auth_token=None):
    """ POST - admin changes """
    # TODO pull in all data about the event and put in the database

    #Get event by ID from DB and send to event view
    event = get_event(event_id)
    return render_template('event_manage.html', event=event, event_auth_token=event_auth_token)

def get_event(id):
    return models.Event.query.filter(models.Event.id == id).first()
