
from orbach.admin import admin

import flask


@admin.route('/')
def index():
    return flask.render_template('admin_index.html')
