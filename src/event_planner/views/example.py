from .. import app

@app.route("/example")
def hello():
    return '''
    <button class='btn btn-primary'>hello</button>
    '''
