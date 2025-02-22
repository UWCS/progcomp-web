"""Add weight column to tests table

Revision ID: dcc5c2df85e7
Revises: e7ae9770dc00
Create Date: 2024-12-29 20:37:32.182113

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dcc5c2df85e7"
down_revision = "e7ae9770dc00"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tests", schema=None) as batch_op:
        batch_op.add_column(sa.Column("weight", sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tests", schema=None) as batch_op:
        batch_op.drop_column("weight")

    # ### end Alembic commands ###
