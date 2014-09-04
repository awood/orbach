from __future__ import print_function, division, absolute_import

import logging
import os

from flask import Flask
from flask.ext.assets import Environment, Bundle
from logging.handlers import RotatingFileHandler


app = Flask(__name__.split('.')[0])
assets = Environment(app)

class OrbachLog(object):
    @staticmethod
    def setup(app):
        handler = RotatingFileHandler('orbach.log', maxBytes=10000, backupCount=2)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if app.debug:
            handler.setLevel(logging.DEBUG)
        else:
            handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)


def read_config():
    return {
        'debug': True
    }


def bundle_js(assets):
    bs_root = 'bootstrap-sass-official/vendor/assets/javascripts/bootstrap'
    js_assets = [
        'jquery/jquery.js',
        '%s/transition.js' % bs_root,
        '%s/alert.js' % bs_root,
        '%s/button.js' % bs_root,
        '%s/tab.js' % bs_root,
        '%s/modal.js' % bs_root,
        '%s/dropdown.js' % bs_root,
        'bootstrap-select/dist/js/bootstrap-select.js',
        'bootstrap-treeview/src/js/bootstrap-treeview.js',
    ]

    if not app.debug:
        filters = 'rjsmin'
    else:
        filters = None

    js = Bundle(*js_assets, filters=filters, output='generated/orbach.min.js')
    assets.register('js_all', js)


def bundle_galleria(assets):
    galleria_assets = [
        'galleria/src'
    ]

    if not app.debug:
        filters = 'rjsmin'
    else:
        filters = None

    galleria = Bundle(*galleria_assets, filters=filters, output='generated/galleria.min.js')
    assets.register('galleria', galleria)


def bundle_css(assets):
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
    css = Bundle(*scss_assets, filters='pyscss', output='generated/orbach.css', depends=('**/*.scss'))

    if not app.debug:
        css = Bundle(css, filters="cssmin")

    assets.register('css_all', css)


def init_app(app, config):
    OrbachLog.setup(app)

    app.config.from_object(config)

    app.debug = app.config['DEBUG']

    assets.debug = app.debug
    assets.url = app.static_url_path
    assets.directory = app.static_folder

    bundle_js(assets)
    bundle_css(assets)

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
