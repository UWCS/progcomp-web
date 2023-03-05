"""review unique constraints

Revision ID: 81752bc872dd
Revises: d7fc0670d403
Create Date: 2023-03-05 14:11:58.735903

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "81752bc872dd"
down_revision = "d7fc0670d403"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("problems", schema=None) as batch_op:
        batch_op.drop_constraint("unq_problems_name", type_="unique")
        batch_op.create_unique_constraint("unq_problem_name", ["name", "progcomp_id"])

    with op.batch_alter_table("progcomps", schema=None) as batch_op:
        batch_op.drop_constraint("unq_progcomp_name", type_="unique")
        batch_op.create_unique_constraint("unq_progcomps_name", ["name"])

    with op.batch_alter_table("teams", schema=None) as batch_op:
        batch_op.drop_constraint("unq_teams_name", type_="unique")
        batch_op.create_unique_constraint("unq_team_name", ["name", "progcomp_id"])

    with op.batch_alter_table("tests", schema=None) as batch_op:
        batch_op.create_unique_constraint("unq_tests_name", ["name", "problem_id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tests", schema=None) as batch_op:
        batch_op.drop_constraint("unq_tests_name", type_="unique")

    with op.batch_alter_table("teams", schema=None) as batch_op:
        batch_op.drop_constraint("unq_team_name", type_="unique")
        batch_op.create_unique_constraint("unq_teams_name", ["name"])

    with op.batch_alter_table("progcomps", schema=None) as batch_op:
        batch_op.drop_constraint("unq_progcomps_name", type_="unique")
        batch_op.create_unique_constraint("unq_progcomp_name", ["name"])

    with op.batch_alter_table("problems", schema=None) as batch_op:
        batch_op.drop_constraint("unq_problem_name", type_="unique")
        batch_op.create_unique_constraint("unq_problems_name", ["name"])

    # ### end Alembic commands ###
