from .. import app, render_template, url_for, request

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new", methods=['POST', 'GET'])
def new():
    if request.method == "POST":
        slotdata = []
        for x in range(0,47):
            slotdata.append(request.form['slot_%s' % x])

        # db.session.add(slotdata)
        # db.session.commit()

        return render_template('index.html')

    daterange = ['12:00 AM', '12:30 AM', '1:00 AM', '1:30 AM', '2:00 AM', '2:30 AM','3:00 AM', '3:30 AM', '4:00 AM', '4:30 AM', '5:00 AM', '5:30 AM', '6:00 AM', '6:30 AM', '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM', '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM']
    daterange24 = ['0:00', '0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
    daterange = enumerate(daterange)
    daterange24 = enumerate(daterange24)
    return render_template('new.html', daterange=daterange, daterange24=daterange24)

@app.route("/event/<event_id>")
@app.route("/event/<event_id>/<event_auth_token>")
def show_event(event_id=None, event_auth_token=None):

    # events.where(event.id == event_id)
    event = {}
    event['name'] = 'Foobar rally'
    event['desc'] = 'fight for your right to bar with your foo'
    event['time'] = '6/9/6969'
    event['participants'] = [('Jenny Swepack', '1-4'), ('Gerald Moneybaby', '6-5')]

    if event_auth_token == None:
        return render_template('event_view.html', event=event)
    else:
        return render_template('event_manage.html', event=event, event_auth_token=event_auth_token)
