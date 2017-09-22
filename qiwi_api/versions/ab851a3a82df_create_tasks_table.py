"""Create tasks table

Revision ID: ab851a3a82df
Revises: f3659271c106
Create Date: 2017-09-13 17:23:10.563515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab851a3a82df'
down_revision = 'f3659271c106'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('date', sa.TIMESTAMP, nullable=False),
        sa.Column('object_link', sa.String, nullable=False),
        sa.Column('amount', sa.String, nullable=False),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey("customers.id"), nullable=False)

    )


def downgrade():
    op.drop_table('tasks')
