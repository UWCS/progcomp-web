"""move to visibility

Revision ID: d7fc0670d403
Revises: 21d2fa22a5d2
Create Date: 2023-03-04 01:41:21.887038

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d7fc0670d403"
down_revision = "21d2fa22a5d2"
branch_labels = ()
depends_on = None

nc = {
    "uq": "unq_%(table_name)s_%(column_0_name)s",
}


def upgrade() -> None:
    visibility_enum = postgresql.ENUM('HIDDEN', 'CLOSED', 'OPEN', name='visibility', create_type=False)
    visibility_enum.create(op.get_bind(), checkfirst=True)

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "problems",
        sa.Column(
            "visibility",
            postgresql.ENUM("HIDDEN", "CLOSED", "OPEN", name="visibility"),
            server_default="OPEN",
            nullable=False,
        ),
    )
    with op.batch_alter_table(
        "problems", schema=None, naming_convention=nc
    ) as batch_op:
        batch_op.drop_column("enabled")
    op.add_column(
        "progcomps",
        sa.Column(
            "visibility",
            sa.Enum("HIDDEN", "CLOSED", "OPEN", name="visibility"),
            server_default="OPEN",
            nullable=False,
        ),
    )
    with op.batch_alter_table(
        "progcomps", schema=None, naming_convention=nc
    ) as batch_op:
        batch_op.drop_column("freeze")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "progcomps",
        sa.Column(
            "freeze", sa.BOOLEAN(), server_default=sa.text("'f'"), nullable=False
        ),
    )
    with op.batch_alter_table(
        "progcomps", schema=None, naming_convention=nc
    ) as batch_op:
        batch_op.drop_column("visibility")
    op.add_column(
        "problems",
        sa.Column(
            "enabled", sa.BOOLEAN(), server_default=sa.text("'t'"), nullable=False
        ),
    )
    with op.batch_alter_table(
        "problems", schema=None, naming_convention=nc
    ) as batch_op:
        batch_op.drop_column("visibility")

    visibility_enum = postgresql.ENUM('HIDDEN', 'CLOSED', 'OPEN', name='visibility', create_type=False)
    visibility_enum.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
