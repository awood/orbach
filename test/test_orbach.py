from flask import Flask
from flask.ext.testing import TestCase

from alembic import context, command
from alembic.config import Config as AlembicConfig

from io import StringIO

from textwrap import dedent

from orbach.config import Config
from orbach import DEFAULT_CONFIG, init_app

from test import temp_file


class OrbachTest(TestCase):
    def config_alembic(self):
        alembic_config = dedent("""
            [alembic]
            sqlalchemy.url = sqlite:///:memory:
            file_template = %%(year)d-%%(month).2d-%%(day).2d-%%(rev)s_%%(slug)s
            script_location = alembic

            [loggers]
            keys = root,sqlalchemy,alembic

            [logger_sqlalchemy]
            level = WARN
            handlers =
            qualname = sqlalchemy.engine

            [logger_alembic]
            level = INFO
            handlers =
            qualname = alembic

            [logger_root]
            level = INFO
            handlers = console
            qualname =

            [handlers]
            keys = console

            [handler_console]
            class = StreamHandler
            # Log to stdout so nosetests can suppress it
            args = (sys.stdout,)
            level = NOTSET
            formatter = generic

            [formatters]
            keys = generic

            [formatter_generic]
            format = %(levelname)-5.5s [%(name)s] %(message)s
        """)
        with temp_file(alembic_config) as config_file:
            alembic_config = AlembicConfig(config_file)
            command.upgrade(alembic_config, "head")

    def create_app(self):
        self.config_alembic()

        test_config = dedent("""
            [orbach]
            debug = False
            logger_name = orbach
            json_as_asii = False
            sqlalchemy_database_uri = sqlite:///:memory:
        """)

        config = Config(StringIO(test_config))
        default_config = Config(StringIO(DEFAULT_CONFIG))

        for item in ["DEBUG"]:
            config.to_boolean(item)
            default_config.to_boolean(item)

        app = Flask("orbach")
        app = init_app(app, (default_config, config))

        return app

    def test_x(self):
        pass
