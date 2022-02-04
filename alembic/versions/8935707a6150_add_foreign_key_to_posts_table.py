"""add foreign-key to posts table

Revision ID: 8935707a6150
Revises: 7fec7d6f05f1
Create Date: 2022-02-03 19:19:33.341516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8935707a6150'
down_revision = '7fec7d6f05f1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table='users', local_cols=["owner_id"], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("posts_users_fk")
    op.drop_column('posts', 'owner_id')
