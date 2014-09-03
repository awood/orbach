from __future__ import print_function, division, absolute_import

import os

from flask import Flask
from flask.ext.assets import Environment, Bundle

from orbach.logger import OrbachLog

app = Flask(__name__.split('.')[0])
assets = Environment(app)


def read_config():
    return {
        'debug': True
    }


def bundle_js(assets):
    js_assets = [
        'jquery/jquery.js',
        'bootstrap-select/dist/js/bootstrap-select.js',
        'bootstrap-sass-official/vendor/assets/javascripts/bootstrap.js',
        'bootstrap-treeview/src/js/bootstrap-treeview.js',
    ]
    js = Bundle(*js_assets, filters='rjsmin', output='generated/orbach.min.js')
    assets.register('js_all', js)


def bundle_scss(assets):
    # TODO Apparently these paths can be placed in a YAML file.  Might be worth doing.
    load_paths = [
        'bootstrap-sass-official/vendor/assets/stylesheets',
        'bootstrap-select/dist/css',
        'bootstrap-treeview/src/css',
        'font-awesome/scss',
    ]
    assets.config['PYSCSS_LOAD_PATHS'] = [os.path.join(assets.directory, d) for d in load_paths]
    scss_assets = [
        'orbach.scss',
    ]
    scss = Bundle(*scss_assets, filters='pyscss', output='generated/orbach.scss', depends=('**/*.scss'))
    assets.register('scss_all', scss)


def init_app(app, config):
    OrbachLog.setup(app)

    app.debug = app.config['DEBUG']

    assets.debug = app.config['DEBUG']
    assets.url = app.static_url_path
    assets.directory = app.static_folder

    bundle_js(assets)
    bundle_scss(assets)

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
