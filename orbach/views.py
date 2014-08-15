from __future__ import print_function, division, absolute_import
from orbach import app


@app.route('/')
def hello():
    return "Hello"
