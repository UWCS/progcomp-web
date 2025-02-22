"""Initial

Revision ID: 8b64d1c837e4
Revises: 
Create Date: 2023-03-01 01:56:57.682998

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8b64d1c837e4"
down_revision = None
branch_labels = ("default",)
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "progcomps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="unq_progcomps_name"),
    )
    op.create_table(
        "problems",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("progcomp_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["progcomp_id"],
            ["progcomps.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="unq_problems_name"),
    )
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("progcomp_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["progcomp_id"],
            ["progcomps.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="unq_teams_name"),
    )
    op.create_table(
        "tests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("problem_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["problems.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("problem_id", sa.Integer(), nullable=True),
        sa.Column("test_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "UNKNOWN",
                "SCORED",
                "CORRECT",
                "PARTIAL",
                "WRONG",
                "INVALID",
                name="status",
            ),
            nullable=True,
        ),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["problems.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.ForeignKeyConstraint(
            ["test_id"],
            ["tests.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("submissions")
    op.drop_table("tests")
    op.drop_table("teams")
    op.drop_table("problems")
    op.drop_table("progcomps")
    # ### end Alembic commands ###
