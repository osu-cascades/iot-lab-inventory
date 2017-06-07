"""empty message

Revision ID: 2a39ff826a00
Revises: 96c6300ec187
Create Date: 2017-06-05 08:05:41.327068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a39ff826a00'
down_revision = '96c6300ec187'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
        sa.Column('is_admin', sa.Boolean(), default=False, nullable=False)
    )


def downgrade():
    op.drop_column('users', 'is_admin')

