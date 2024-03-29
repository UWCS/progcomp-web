"""move to visibility

Revision ID: d7fc0670d403
Revises: 21d2fa22a5d2
Create Date: 2023-03-04 01:41:21.887038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7fc0670d403'
down_revision = '21d2fa22a5d2'
branch_labels = ()
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('problems', sa.Column('visibility', sa.Enum('HIDDEN', 'CLOSED', 'OPEN', name='visibility'), server_default='OPEN', nullable=False))
    op.drop_column('problems', 'enabled')
    op.add_column('progcomps', sa.Column('visibility', sa.Enum('HIDDEN', 'CLOSED', 'OPEN', name='visibility'), server_default='OPEN', nullable=False))
    op.drop_column('progcomps', 'freeze')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('progcomps', sa.Column('freeze', sa.BOOLEAN(), server_default=sa.text("'f'"), nullable=False))
    op.drop_column('progcomps', 'visibility')
    op.add_column('problems', sa.Column('enabled', sa.BOOLEAN(), server_default=sa.text("'t'"), nullable=False))
    op.drop_column('problems', 'visibility')
    # ### end Alembic commands ###
