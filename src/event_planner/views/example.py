from .. import app, render_template, url_for

@app.route("/example")
def hello():
    return render_template('example.html')
