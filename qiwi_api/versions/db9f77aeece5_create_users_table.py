"""Create users table

Revision ID: db9f77aeece5
Revises: 
Create Date: 2017-09-13 17:18:03.326952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db9f77aeece5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('vk_id', sa.String, nullable=False),
        sa.Column('qiwi_wallet', sa.String(11), nullable=False),
    )


def downgrade():
    op.drop_table('users')
