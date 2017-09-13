from .. import app, render_template, url_for

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new")
def new():
    return render_template('new.html')

@app.route("/event/<event_id>")
def show_event(event_id):
    return 'Event %d' % event_id