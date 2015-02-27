

import unittest
import os

# We need to import this model to set up the foreign key pragma
from orbach import model

from alembic.config import Config as AlembicConfig
from alembic.context import EnvironmentContext
from alembic.script import ScriptDirectory

from sqlalchemy import engine_from_config, pool, MetaData

import logging
from sqlalchemy.exc import IntegrityError
logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.INFO)
logging.getLogger('orbach').setLevel(logging.INFO)


class SchemaTest(unittest.TestCase):
    def setUp(self):
        config = AlembicConfig(os.path.join(os.getcwd(), 'alembic.ini'))
        config.set_main_option('sqlalchemy.url', 'sqlite://')
        script_dir = ScriptDirectory.from_config(config)

        metadata = MetaData(naming_convention=model.metadata_convention)

        self.engine = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool)

        self.conn = self.engine.connect()

        self.context = EnvironmentContext(
            config,
            script_dir,
        )

        def upgrade(rev, context):
            return script_dir._upgrade_revs('head', rev)

        self.context.configure(
            connection=self.conn,
            target_metadata=metadata,
            fn=upgrade,
        )

        with self.context.begin_transaction():
            self.context.run_migrations()

    def test_admin_user_exists(self):
        result = self.conn.execute("""
            SELECT username FROM users
        """).fetchall()
        self.assertEqual(1, len(result))

    def test_admin_user_is_admin_role(self):
        result = self.conn.execute("""
            SELECT r.name FROM users u, roles r
            WHERE u.username = 'admin' and u.role_id = r.id
        """).fetchall()
        self.assertEquals(1, len(result))
        self.assertEqual("ADMIN", result[0][0])

    def test_cover_within_gallery(self):
        for db_id in [1, 2]:
            self.conn.execute("INSERT INTO galleries (id, name, description) VALUES (%d, 'name', 'description')" % db_id)
            self.conn.execute("INSERT INTO image_files (id, file, created_by) VALUES (%d, 'filename', 1)" % db_id)

        self.conn.execute("INSERT INTO pictures (id, title, caption, image_file_id, gallery_id) VALUES (1, 'title', 'caption', 1, 1)")
        self.conn.execute("INSERT INTO pictures (id, title, caption, image_file_id, gallery_id) VALUES (2, 'title', 'caption', 2, 2)")

        self.conn.execute("INSERT INTO covers (id, picture_id, gallery_id) VALUES (1, 1, 1)")

        # Try to create a cover using a picture not in the gallery
        with self.assertRaises(IntegrityError):
            self.conn.execute("INSERT INTO covers (id, picture_id, gallery_id) VALUES (2, 1, 2)")

    def tearDown(self):
        self.conn.close()
