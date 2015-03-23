from orbach.api import api
from orbach.controller import GalleryController, UserController
from orbach.version import __version__

from flask.views import MethodView
from flask import jsonify


@api.route('/')
def status():
    return jsonify({"API Version": __version__})


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    api.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    api.add_url_rule(url, view_func=view_func, methods=['POST'])
    api.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


def user_required(func):
    def decorator(*args, **kwargs):
        # TODO if not authenticated
        return func(*args, **kwargs)
    return decorator


class GalleryApi(MethodView):
    decorators = [user_required]

    def get(self, gal_id):
        if gal_id is None:
            res = {"galleries": GalleryController.get_all()}
        else:
            res = {"gallery": GalleryController(gal_id).get()}
        return jsonify(res)

    def post(self):
        res = GalleryController.create(None)
        return jsonify({"gallery": res})

    def put(self, gal_id):
        res = GalleryController(gal_id).update()
        return jsonify({"gallery": res})

    def delete(self, gal_id):
        res = GalleryController(gal_id).delete()
        if res:
            return ('', 204)
        else:
            return ('', 404)


register_api(GalleryApi, "gallery_api", "/galleries/", pk="gal_id")


class UserApi(MethodView):
    decorators = [user_required]

    def get(self, user_id):
        if user_id is None:
            res = {"users": UserController.get_all()}
        else:
            res = {"user": UserController(user_id).get()}
        return jsonify(res)

    def post(self):
        res = UserController.create(None)
        return jsonify({"user": res})

    def put(self, user_id):
        res = UserController(user_id).update()
        return jsonify({"user": res})

    def delete(self, user_id):
        res = UserController(user_id).delete()
        if res:
            return ("", 204)
        else:
            return ("", 404)


register_api(UserApi, "user_api", "/users/", pk="user_id")
