from .. import app, render_template, url_for

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new")
def new():
    return render_template('new.html')

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