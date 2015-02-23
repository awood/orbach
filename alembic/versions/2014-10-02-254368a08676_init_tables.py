"""Create initial tables

Revision ID: 254368a08676
Revises: None
Create Date: 2014-10-02 22:18:16.145622

"""

# revision identifiers, used by Alembic.
revision = '254368a08676'
down_revision = None

from alembic import op
import sqlalchemy as sa

import bcrypt


def id():
    return sa.Column('id', sa.Integer, primary_key=True)

def created():
    return sa.Column('created', sa.DateTime, server_default=sa.func.now())

def modified():
    return sa.Column('modified', sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())

def upgrade():
    current_context = op.get_context()
    meta = current_context.opts['target_metadata']

    # Note that we need to provide the MetaData object here.
    roles = sa.Table('roles', meta,
        id(),
        sa.Column('name', sa.Unicode(50), nullable=False),
        sa.Column('description', sa.Unicode(500)),
        created(),
        modified(),
    )
    roles.create(op.get_bind())

    op.bulk_insert(roles, [
            {'id': 1, 'name': u'ADMIN', 'description': u'Administrator'},
        ],
        multiinsert=False
    )

    users = sa.Table('users', meta,
        id(),
        sa.Column('username', sa.Unicode(50), nullable=False),
        sa.Column('password', sa.String(60), nullable=False),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')),
        created(),
        modified(),
    )
    users.create(op.get_bind())

    password = bcrypt.hashpw('admin', bcrypt.gensalt())
    op.bulk_insert(users, [
            {'id': 1, 'username': u'admin', 'password': password, 'role_id': '1'},
        ],
        multiinsert=False
    )

    galleries = sa.Table('galleries', meta,
        id(),
        sa.Column('name', sa.Unicode(175), nullable=False),
        sa.Column('description', sa.Unicode(1000)),
        sa.Column('parent', sa.Integer),
        created(),
        modified(),
    )
    galleries.create(op.get_bind())

    images = sa.Table('image_files', meta,
        id(),
        sa.Column('file', sa.Unicode(300), nullable=False),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id')),
        created(),
        modified(),
    )
    images.create(op.get_bind())

    # TODO Add cascade deletes for pictures/covers
    # We have to add the unique constraint to satisfy a sqlite quirk
    # See https://www.sqlite.org/foreignkeys.html and http://stackoverflow.com/a/7542427
    pictures = sa.Table('pictures', meta,
        id(),
        sa.Column('title', sa.Unicode(300)),
        sa.Column('caption', sa.Unicode(1500)),
        sa.Column('image_file_id', sa.Integer, sa.ForeignKey('image_files.id')),
        sa.Column('gallery_id', sa.Integer, sa.ForeignKey('galleries.id')),
        sa.UniqueConstraint('id', 'gallery_id'),
        created(),
        modified(),
    )
    pictures.create(op.get_bind())

    covers = sa.Table('covers', meta,
        id(),
        sa.Column('picture_id', sa.Integer),
        sa.Column('gallery_id', sa.Integer),
        sa.schema.ForeignKeyConstraint(
            ['picture_id', 'gallery_id'], ['pictures.id', 'pictures.gallery_id']
        ),
        created(),
        modified(),
    )
    covers.create(op.get_bind())


def downgrade():
    op.drop_table("pictures")
    op.drop_table("galleries")
    op.drop_table("users")
    op.drop_table("roles")
