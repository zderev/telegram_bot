"""Create customers table

Revision ID: f3659271c106
Revises: db9f77aeece5
Create Date: 2017-09-13 17:21:39.415823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3659271c106'
down_revision = 'db9f77aeece5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('qiwi_wallet', sa.String(11), nullable=False),
    )


def downgrade():
    op.drop_table('customers')
