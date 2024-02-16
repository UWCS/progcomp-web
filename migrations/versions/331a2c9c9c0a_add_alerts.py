"""add alerts

Revision ID: 331a2c9c9c0a
Revises: 81752bc872dd
Create Date: 2023-03-05 15:48:28.952941

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "331a2c9c9c0a"
down_revision = "81752bc872dd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("progcomp_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["progcomp_id"],
            ["progcomps.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "progcomp_id", name="unq_alerts_name"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("alerts")
    # ### end Alembic commands ###