from __future__ import print_function, division, absolute_import
from flask import Flask
from orbach.logger import OrbachLog

app = Flask(__name__.split('.')[0])


def read_config():
    return {
        'debug': True
    }


def init_app(app, config):
    app.debug = config['debug']

    OrbachLog.setup(app)

    from orbach.gallery import gallery as gallery_blueprint
    app.register_blueprint(gallery_blueprint)

    from orbach.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    app.logger.debug("Orbach initialized")
    return app


def main():
    return init_app(app, read_config())

if __name__ != "__main__":
    # Twisted/Gunicorn/etc will take this path
    app = main()
