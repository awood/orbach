"""create gallery table

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


def upgrade():
    current_context = op.get_context()
    meta = current_context.opts['target_metadata']

    # Note that we need to provide the MetaData object here.
    roles = sa.Table('roles', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(50), nullable=False),
        sa.Column('description', sa.Unicode(500))
    )
    roles.create(op.get_bind())

    op.bulk_insert(roles, [
            {'id': 1, 'name': 'ADMIN', 'description': 'Administrator'},
        ],
        multiinsert=False
    )

    users = sa.Table('users', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.Unicode(50), nullable=False),
        sa.Column('password', sa.String(60), nullable=False),
        sa.Column('role', sa.Integer, sa.ForeignKey('roles.id'))
    )
    users.create(op.get_bind())

    password = bcrypt.hashpw('admin', bcrypt.gensalt())
    op.bulk_insert(users, [
            {'id': 1, 'username': 'admin', 'password': password, 'role': '1'},
        ],
        multiinsert=False
    )

    galleries = sa.Table('galleries', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(175), nullable=False),
        sa.Column('description', sa.Unicode(1000)),
        sa.Column('parent', sa.Integer),
        sa.Column('created', sa.DATETIME, server_default=sa.func.now()),
        sa.Column('modified', sa.DATETIME, server_default=sa.func.now(), server_onupdate=sa.func.now()),
    )
    galleries.create(op.get_bind())

    images = sa.Table('images', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('file', sa.Unicode(300), nullable=False),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id'))
    )
    images.create(op.get_bind())

    # TODO Add cascade deletes for pictures/covers
    pictures = sa.Table('pictures', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Unicode(300)),
        sa.Column('caption', sa.Unicode(1500)),
        sa.Column('image_id', sa.Integer, sa.ForeignKey('images.id')),
        sa.Column('gallery_id', sa.Integer, sa.ForeignKey('galleries.id'))
    )
    pictures.create(op.get_bind())

    covers = sa.Table('covers', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('picture_id', sa.Integer),
        sa.Column('gallery_id', sa.Integer),
        sa.schema.ForeignKeyConstraint(
            ['picture_id', 'gallery_id'], ['pictures.id', 'pictures.gallery_id']
        )
    )
    covers.create(op.get_bind())


def downgrade():
    op.drop_table("pictures")
    op.drop_table("galleries")
    op.drop_table("users")
    op.drop_table("roles")
