from .. import db, models, app, render_template, url_for, request
from flask import flash, redirect
from datetime import date as dt

@app.route("/")
def index():
    event = {}
    event['name'] = "Software Party!"
    event['date'] = '9/18/2017'
    event['description'] = "Software party for the EECS 448 students."
    event['admin'] = "Kitchen Utensils Team"

    #TESTING
    event1 = {}
    event1['name'] = "Dinner Date"
    event1['date'] = '9/19/2017'
    event1['description'] = "Dinner date with the finest utensils"
    event1['admin'] = "Gerald Moneybaby"

    events = (event, event1)

    return render_template('index.html', events=events)

@app.route("/new", methods=['GET'])
def new_get():

    #Create the dates to show in the template for iterator.
    daterange = ['12:00 AM', '12:30 AM', '1:00 AM', '1:30 AM', '2:00 AM', '2:30 AM','3:00 AM', '3:30 AM', '4:00 AM', '4:30 AM', '5:00 AM', '5:30 AM', '6:00 AM', '6:30 AM', '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM', '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM']
    daterange24 = ['0:00', '0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
    daterange = enumerate(daterange)
    return render_template('new.html', daterange=daterange, daterange24=daterange24)

@app.route("/new", methods=['POST'])
def new_post():
    #Variable for recording error in form parsing to prevent back commit to db
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

    #commit to db if no error.
    if not error:
        event = models.Event(name, desc, event_date)
        db.session.add(event)
        db.session.commit()

    return redirect(url_for('new_get'))

@app.route("/event/<event_id>", methods=['GET'])
def show_event_get(event_id):
    """ GET - user view """
    events = models.Event.query.filter(id == event_id).first()


    # events.where(event.id == event_id)
    event = {}
    event['name'] = 'Foobar rally'
    event['desc'] = 'fight for your right to bar with your foo'
    event['time'] = '6/9/6969'
    event['participants'] = [('Jenny Swepack', '1-4'), ('Gerald Moneybaby', '6-5')]

    return render_template('event_view.html', event=events)


@app.route("/event/<event_id>", methods=['POST'])
def show_event_post(event_id=None):
    """ POST - user adds participation """

@app.route("/event/<event_id>/<event_auth_token>", methods=['GET'])
def show_event_get_admin(event_id=None, event_auth_token=None):
    """ GET - admin view """

@app.route("/event/<event_id>/<event_auth_token>", methods=['POST'])
def show_event_post_admin(event_id=None, event_auth_token=None):
    """ POST - admin changes """
    