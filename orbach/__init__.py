#! /usr/bin/env python

from flask import Flask

app = Flask(__name__)

import orbach.views

if __name__ == '__main__':
    app.run()
