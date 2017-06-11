"""empty message

Revision ID: 84da7c02983d
Revises: 3121e863bc9c
Create Date: 2017-06-07 20:00:00.959441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84da7c02983d'
down_revision = '3121e863bc9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('part_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['part_id'], ['parts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    # ### end Alembic commands ###