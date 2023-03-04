"""review unique constraints

Revision ID: 81752bc872dd
Revises: d7fc0670d403
Create Date: 2023-03-04 03:44:29.853970

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "81752bc872dd"
down_revision = "d7fc0670d403"
branch_labels = ()
depends_on = None

naming_convention = {
    "uq": "unq_%(table_name)s_%(column_0_name)s",
}


def upgrade() -> None:
    with op.batch_alter_table("problems", naming_convention=naming_convention) as bop:
        bop.drop_constraint("unq_problems_name")
        bop.create_unique_constraint("unq_problems_name", ["name", "progcomp_id"])

    with op.batch_alter_table("teams") as bop:
        bop.drop_constraint("unq_teams_name")
        bop.create_unique_constraint("unq_teams_name", ["name", "progcomp_id"])

    with op.batch_alter_table("tests") as bop:
        bop.create_unique_constraint("unq_tests_name", ["name", "problem_id"])


def downgrade() -> None:
    with op.batch_alter_table("problems") as bop:
        bop.drop_constraint("unq_problems_name")
        bop.create_unique_constraint("unq_problems_name", ["name"])

    with op.batch_alter_table("teams") as bop:
        bop.drop_constraint("unq_teams_name")
        bop.create_unique_constraint("unq_teams_name", ["name"])

    with op.batch_alter_table("tests") as bop:
        bop.drop_constraint("unq_tests_name")
