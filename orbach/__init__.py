import logging
import os

from flask import Flask, json
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy, Model, _BoundDeclarativeMeta

from logging.handlers import RotatingFileHandler

from textwrap import dedent
from io import StringIO

from pathlib import Path

from orbach.config import Config

DEFAULT_CONFIG = dedent("""
[orbach]
application_root = /var/lib/orbach

[flask]
DEBUG = False
TESTING = False
LOGGER_NAME = orbach
JSON_AS_ASII = False
SQLALCHEMY_DATABASE_URI = sqlite:///%(current_dir)s
""") % {
    "current_dir": os.path.join(os.path.abspath(os.path.dirname(__file__)), "orbach.db")
}

app = Flask(__name__.split('.')[0])

LOG_FORMAT = '%(asctime)s [%(levelname)s] (%(name)s:%(module)s:%(lineno)d) %(message)s'


class OrbachLog(object):
    @staticmethod
    def setup(app):
        app.debug_log_format = LOG_FORMAT
        handler = RotatingFileHandler('orbach.log', maxBytes=5000000, backupCount=2)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)


class OrbachEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "to_json"):
            return o.to_json()
        return super().default(self, o)


class DbMeta(_BoundDeclarativeMeta):
    """Python meta-class for creating the SQLAlchemy declarative base

    The SQLAlchemy object returned from Flask SQLAlchemy has all sorts of classes defined
    in it that bind to the database context.

    The recommended way to do things is to define a "db" at the module level and then all
    model objects inherit from that.  Unfortunately, we need to read the configuration
    and do all other stuff first.  Plus, I don't like doing things like that at the module
    level: it makes testing difficult.

    So instead, we define a meta-class inheriting from the SQLAlchemy meta-class used to
    construct the bound classes.  Our meta-class has an attribute containing the SQLAlchemy
    object.  Then we set the base class from an unbound class to the equivalent
    bound class (e.g. from flask.ext.sqlalchemy.Model to db.Model) and then hand off control
    back to the SQLAlchemy meta-class.

    Finally, we import the model module which begins the construction of everything.
    Thus, we have a class with the correct inheritance set at runtime.

    Another solution would be

    def start_app(self):
        ...
        db = SQLAlchemy(app)
        __builtin__.__dict__["my_db"] = db

    And then all model classes could inherit from "my_db.Model".  This solution has the
    disadvantage of throwing warnings in static analysis since the "my_db" builtin is not
    normally present.
    """
    db = None

    def __new__(cls, name, bases, dct):
        if DbMeta.db:
            bases_list = list(bases)
            if Model in bases_list:
                bases_list.insert(bases_list.index(Model), DbMeta.db.Model)
            bases = tuple(bases_list)
        return super(DbMeta, cls).__new__(cls, name, bases, dct)


def read_config(config_file):
    try:
        stream = open(config_file, 'r')
    except Exception:
        raise IOError("Failed to open %s" % config_file)

    orbach_config = Config(stream)
    default_config = Config(StringIO(DEFAULT_CONFIG))

    for k, v in default_config:
        if k not in orbach_config:
            orbach_config[k] = v

    flask_config = default_config.flask_config().copy()
    flask_config.update(orbach_config.flask_config())

    return (flask_config, orbach_config)


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


def init_db(app):
    db = SQLAlchemy(app)
    DbMeta.db = db
    # Import this so SQLAlchemy listeners will get attached
    from orbach import alchemy_util  # NOQA
    from orbach import model  # NOQA
    return db


def init_root_dir(app):
    p = Path(app.config.orbach["application_root"])
    try:
        Path.mkdir(p, parents=True)
    except FileExistsError:
        pass
    app.logger.info("Working in %s" % p)


def init_app(app, config):
    OrbachLog.setup(app)

    flask_config, orbach_config = config

    app.config.update(flask_config)

    app.config.orbach = orbach_config
    app.logger.debug("Running with configuration: %s" % app.config)

    app.db = init_db(app)
    init_root_dir(app)

    app.json_encoder = OrbachEncoder

    assets = Environment(app)
    assets.debug = app.config['DEBUG']
    assets.url = app.static_url_path
    assets.directory = app.static_folder

    bundle_js(assets)
    bundle_css(assets)

    from orbach.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    from orbach.gallery import gallery as gallery_blueprint
    app.register_blueprint(gallery_blueprint)

    from orbach.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    app.logger.info("Orbach is ready!")
    return app


def init_from_file(config_file):
    return init_app(app, read_config(config_file))
