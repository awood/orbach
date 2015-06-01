from orbach.api import api
from orbach.controller import GalleryController, UserController, ImageFileController
from orbach.version import __version__

from flask.ext.restful import Resource
from flask import jsonify, request
from flask.ext.babel import _, get_locale


def authn_required(func):
    def decorator(*args, **kwargs):
        # TODO if not authenticated
        return func(*args, **kwargs)
    return decorator


@api.resource("/")
class StatusApi(Resource):
    def get(self):
        return jsonify({
            _("Application Version"): __version__,
            _("API Version"): "1.0",
            _("Request Locale"): str(get_locale()),
        })


@api.resource("/image_file/", "/image_file/<int:image_file_id>")
class ImageFileApi(Resource):
    def get(self, image_id):
        if image_id is None:
            files = ImageFileController.get_all()
        else:
            files = ImageFileController(image_id).get()
        return jsonify({'image_files': files})

    def post(self):
        res = ImageFileController.create(request)
        return jsonify(res)


@api.resource("/gallery/", "/gallery/<int:gallery_id>")
class GalleryApi(Resource):
    def get(self, gal_id):
        if gal_id is None:
            galleries = GalleryController.get_all()
        else:
            galleries = GalleryController(gal_id).get()
        return jsonify({'galleries': galleries})

    def post(self):
        post_data = request.get_json()
        res = GalleryController.create(post_data)
        return jsonify({"gallery": res})

    def put(self, gal_id):
        post_data = request.get_json()
        res = GalleryController(gal_id).update(post_data)
        return jsonify({"gallery": res})

    def delete(self, gal_id):
        res = GalleryController(gal_id).delete()
        if res:
            return ('', 204)
        else:
            return ('', 404)


@api.resource("/user/", "/users/<int:user_id>")
class UserApi(Resource):
    def get(self, user_id):
        if user_id is None:
            users = UserController.get_all()
        else:
            users = UserController(user_id).get()
        return jsonify({'users': users})

    def post(self):
        post_data = request.get_json()
        res = UserController.create(post_data)
        return jsonify({"user": res})

    def put(self, user_id):
        post_data = request.get_json()
        res = UserController(user_id).update(post_data)
        return jsonify({"user": res})

    def delete(self, user_id):
        res = UserController(user_id).delete()
        if res:
            return ("", 204)
        else:
            return ("", 404)
