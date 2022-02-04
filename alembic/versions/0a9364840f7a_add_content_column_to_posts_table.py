"""add content column to posts table

Revision ID: 0a9364840f7a
Revises: 93c22c0437fa
Create Date: 2022-02-03 18:59:20.159065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a9364840f7a'
down_revision = '93c22c0437fa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
