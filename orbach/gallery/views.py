from __future__ import print_function, division, absolute_import
from orbach.gallery import gallery

import flask


@gallery.route('/')
def index():
    return flask.render_template('index.html')
