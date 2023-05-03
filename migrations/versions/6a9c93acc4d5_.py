"""empty message

Revision ID: 6a9c93acc4d5
Revises: 3a5d5674ae9b
Create Date: 2023-04-17 12:05:36.502548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a9c93acc4d5'
down_revision = '3a5d5674ae9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('character', sa.String(length=120), nullable=False),
    sa.Column('planets', sa.String(length=120), nullable=False),
    sa.Column('vehicles', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('favorites')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorites', sa.VARCHAR(length=120), autoincrement=False, nullable=True))

    op.drop_table('favorite')
    # ### end Alembic commands ###