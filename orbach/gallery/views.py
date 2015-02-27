from orbach.gallery import gallery

import flask


@gallery.route('/')
def index():
    return flask.render_template('gallery_index.html')
