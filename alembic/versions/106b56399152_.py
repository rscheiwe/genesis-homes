"""empty message

Revision ID: 106b56399152
Revises: 7506120abb1b
Create Date: 2023-02-09 14:39:10.292062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '106b56399152'
down_revision = '7506120abb1b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userroles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_name', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userroles', schema=None) as batch_op:
        batch_op.drop_column('role_name')

    # ### end Alembic commands ###
