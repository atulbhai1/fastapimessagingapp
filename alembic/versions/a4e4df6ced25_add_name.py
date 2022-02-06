"""add-name

Revision ID: a4e4df6ced25
Revises: bd4ac7853e8e
Create Date: 2022-02-05 21:26:34.241881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4e4df6ced25'
down_revision = 'bd4ac7853e8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'users', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'name')
    # ### end Alembic commands ###