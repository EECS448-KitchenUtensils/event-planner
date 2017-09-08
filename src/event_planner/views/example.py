from .. import app

@app.route("/example")
def hello():
    return "hello world!"
