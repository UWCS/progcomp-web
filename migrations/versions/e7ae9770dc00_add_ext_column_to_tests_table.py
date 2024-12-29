"""Add ext column to tests table

Revision ID: e7ae9770dc00
Revises: 331a2c9c9c0a
Create Date: 2024-12-28 15:43:45.870609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7ae9770dc00'
down_revision = '331a2c9c9c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ext', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tests', schema=None) as batch_op:
        batch_op.drop_column('ext')

    # ### end Alembic commands ###
