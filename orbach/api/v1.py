from orbach.api import api
from orbach.controller import GalleryController, UserController, ImageFileController
from orbach.version import __version__

from flask.views import MethodView
from flask import jsonify, request
from flask.ext.babel import _, get_locale


@api.route('/')
def status():
    return jsonify({
        _("Application Version"): __version__,
        _("API Version"): "1.0",
        _("Request Locale"): str(get_locale()),
    })


def authn_required(func):
    def decorator(*args, **kwargs):
        # TODO if not authenticated
        return func(*args, **kwargs)
    return decorator


def register_api(view, endpoint, url, pk='id', pk_type='int', authn=True):
    # TODO Maybe make authn finer-grain by sending in a list with HTTP verbs
    # and only apply the decorator to URL rules using those verbs
    view_func = view.as_view(endpoint)
    api.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    api.add_url_rule(url, view_func=view_func, methods=['POST'])
    api.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
        methods=['GET', 'PUT', 'DELETE'])


class ImageFileApi(MethodView):
    def get(self, image_id):
        if image_id is None:
            files = ImageFileController.get_all()
        else:
            files = ImageFileController(image_id).get()
        return jsonify({'image_files': files})

    def post(self):
        res = ImageFileController.create(request)
        return jsonify(res)


register_api(ImageFileApi, "image_file_api", "/image_files/", pk="image_file_id")


class GalleryApi(MethodView):
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


register_api(GalleryApi, "gallery_api", "/galleries/", pk="gal_id")


class UserApi(MethodView):
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


register_api(UserApi, "user_api", "/users/", pk="user_id")
