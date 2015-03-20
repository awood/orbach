import os

from tempfile import NamedTemporaryFile

from flask.ext.testing import TestCase

from alembic import command
from alembic.config import Config as AlembicConfig

from textwrap import dedent

from orbach import init_from_file

from test import temp_file


class OrbachTest(TestCase):
    def run_alembic(self):
        # Creating a temp file for the DB for every test is pretty inefficient
        # but I couldn't figure out a way to tell SQLAlchemy to connect to a shared
        # in-memory db.  The in-memory db needs to be shared because first Alembic needs
        # to connect, and then the Flask SQLAlchemy stuff.
        # See http://stackoverflow.com/questions/27910829 for someone with the same
        # issue
        self.db_file = NamedTemporaryFile(delete=False, prefix="orbach_test_db_").name
        alembic_config_content = dedent("""
            [alembic]
            sqlalchemy.url = sqlite:///{temp_db_file}
            file_template = %%(year)d-%%(month).2d-%%(day).2d-%%(rev)s_%%(slug)s
            script_location = alembic

            [loggers]
            keys = root,sqlalchemy,alembic

            [logger_sqlalchemy]
            level = INFO
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
        """).format(temp_db_file=self.db_file)
        with temp_file(alembic_config_content) as config_file:
            alembic_config = AlembicConfig(config_file)
            command.upgrade(alembic_config, "head")

    def create_app(self):
        self.run_alembic()

        test_config = dedent("""
            [orbach]

            [flask]
            DEBUG = False
            TESTING = True
            LOGGER_NAME = orbach
            SQLALCHEMY_DATABASE_URI = sqlite:///{temp_db_file}
        """).format(temp_db_file=self.db_file)

        self.config_file = NamedTemporaryFile(delete=False, prefix="orbach_test_config_").name
        with open(self.config_file, 'w') as f:
            f.write(test_config)

        app = init_from_file(self.config_file)
        return app

    def tearDown(self):
        self.app.db.session.remove()
        os.unlink(self.db_file)
        os.unlink(self.config_file)

    def test_x(self):
        pass

    def test_y(self):
        pass
