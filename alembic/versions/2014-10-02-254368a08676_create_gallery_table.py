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


def upgrade():
    op.create_table("galleries",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(175), nullable=False),
        sa.Column('description', sa.Unicode(1000))
    )


def downgrade():
    op.drop_table("galleries")
