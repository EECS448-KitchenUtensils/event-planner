from .. import app, render_template, url_for

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new")
def new():
    daterange = ['12:00 AM', '12:30 AM', '1:00 AM', '1:30 AM', '2:00 AM', '2:30 AM','3:00 AM', '3:30 AM', '4:00 AM', '4:30 AM', '5:00 AM', '5:30 AM', '6:00 AM', '6:30 AM', '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM', '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM']
    daterange = enumerate(daterange)
    return render_template('new.html', daterange=daterange)

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