"""create post table

Revision ID: 93c22c0437fa
Revises: 
Create Date: 2022-01-03 17:38:39.873696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93c22c0437fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False),)


def downgrade():
    op.drop_table('posts')
