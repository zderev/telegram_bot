"""Create tasks_to_users table

Revision ID: 4900ad8807d9
Revises: ab851a3a82df
Create Date: 2017-09-13 17:30:37.686647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4900ad8807d9'
down_revision = 'ab851a3a82df'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks_to_users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey("tasks.id"),nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )



def downgrade():
    pass
