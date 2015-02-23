from __future__ import print_function, division, absolute_import

import logging
import os

from flask import Flask
from flask.ext.assets import Environment, Bundle

from logging.handlers import RotatingFileHandler

from textwrap import dedent
from io import StringIO

from orbach.config import Config
from orbach import model
from __builtin__ import OSError


DEFAULT_CONFIG = dedent(u"""
[orbach]
debug = False
logger_name = orbach
json_as_asii = False
sqlalchemy_database_uri = "sqlite:///%(current_dir)s"
""") % {
    "current_dir": os.path.join(os.path.abspath(os.path.dirname(__file__)), "orbach.db")
}

app = Flask(__name__.split('.')[0])
assets = Environment(app)

LOG_FORMAT = '%(asctime)s [%(name)s(%(module)s:%(lineno)d)] %(message)s'


class OrbachLog(object):
    @staticmethod
    def setup(app):
        app.debug_log_format = LOG_FORMAT
        handler = RotatingFileHandler('orbach.log', maxBytes=5000000, backupCount=2)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)


def read_config(config_file):
    try:
        stream = open(config_file, 'r')
    except Exception:
        raise IOError("Failed to open %s" % config_file)

    config = Config(stream)
    default_config = Config(StringIO(DEFAULT_CONFIG))

    for item in ["DEBUG"]:
        config.to_boolean(item)
        default_config.to_boolean(item)

    return (default_config, config)


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


def init_app(app, config_list):
    OrbachLog.setup(app)
    for c in config_list:
        app.config.from_object(c)
        app.logger.debug("Loaded %s" % c)
    app.logger.debug("Running with configuration: %s" % app.config)

    assets.debug = app.debug
    assets.url = app.static_url_path
    assets.directory = app.static_folder

    bundle_js(assets)
    bundle_css(assets)

    from orbach.gallery import gallery as gallery_blueprint
    app.register_blueprint(gallery_blueprint)

    from orbach.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    app.logger.info("Orbach is ready!")
    return app


def init_from_file(config_file):
    (default_config, config) = read_config(config_file)
    return init_app(app, [default_config, config])
