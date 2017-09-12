from .. import app, render_template, url_for

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new")
def new():
    return render_template('new.html')