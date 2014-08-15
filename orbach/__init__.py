from __future__ import print_function, division, absolute_import
from flask import Flask

app = Flask(__name__.split('.')[0])

import orbach.views
