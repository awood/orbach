#! /usr/bin/env python

from flask import Flask

app = Flask(__name__.split('.')[0])

import orbach.views
