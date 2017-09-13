from .. import app, render_template, url_for

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new")
def new():
    return render_template('new.html')

@app.route("/event/<event_id>")
def show_event(event_id):
    # events.where(event.id == event_id)
    return render_template('event.html', event_id=event_id)