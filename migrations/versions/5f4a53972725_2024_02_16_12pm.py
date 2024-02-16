"""2024-02-16 12pm

Revision ID: 5f4a53972725
Revises: 5a9058b825d3
Create Date: 2024-02-16 11:54:42.549206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f4a53972725'
down_revision = '5a9058b825d3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tests", sa.Column("ext", sa.String(), nullable=False))


def downgrade():
    op.drop_column("tests", "ext")
