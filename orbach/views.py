from orbach import app


@app.route('/')
def hello():
    return "Hello"
