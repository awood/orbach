from orbach import app
from orbach.api import api
from orbach.controller import GalleryController
from orbach.version import __version__

from flask.views import View
from flask import request, jsonify


@api.route('/')
def index():
    return jsonify({"API Version": __version__})


class GalleryApiView(View):
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def dispatch_request(self, *args, **kwargs):
        gc = GalleryController(None)
        if request.method == 'GET':
            gal = gc.get(*args, **kwargs)
        elif request.method == 'POST':
            gal = gc.create(*args, **kwargs)
        elif request.method == 'PUT':
            gal = gc.modify(*args, **kwargs)
        elif request.method == 'DELETE':
            gal = gc.delete(*args, **kwargs)

        return jsonify(gal)


app.add_url_rule("/gallery", view_func=GalleryApiView.as_view("gallery_api_view"))
app.add_url_rule("/gallery/<int:id>", view_func=GalleryApiView.as_view("gallery_api_view_id"))
