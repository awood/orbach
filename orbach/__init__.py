from __future__ import print_function, division, absolute_import

from flask import Flask
from flask.ext.assets import Environment, Bundle

from orbach.logger import OrbachLog

app = Flask(__name__.split('.')[0])


def read_config():
    return {
        'debug': True
    }


def init_app(app, config):
    app.debug = config['debug']

    OrbachLog.setup(app)

    assets = Environment(app)
    js_assets = [
        'jquery/jquery.js',
        'bootstrap-select/dist/js/bootstrap-select.js',
        'bootstrap-sass-official/assets/javascripts/bootstrap.js',
        'bootstrap-treeview/src/js/bootstrap-treeview.js',
    ]
    js = Bundle(*js_assets, filters='jsmin', output='generated/orbach.min.js')
    assets.register('js_all', js)

    from orbach.gallery import gallery as gallery_blueprint
    app.register_blueprint(gallery_blueprint)

    from orbach.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    return app


def main():
    return init_app(app, read_config())

if __name__ != "__main__":
    # Twisted/Gunicorn/etc will take this path
    app = main()
