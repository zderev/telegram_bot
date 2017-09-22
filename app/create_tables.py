# NEW VERSION

from alembic import op
import sqlalchemy as sa

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:open@localhost/qiwi_api')
metadata = sa.MetaData()
customers_table = sa.Table(
    'customers', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('customer_id', sa.Integer, nullable=False),
    sa.Column('qiwi_wallet', sa.String(11), nullable=False),
)

task_table = sa.Table(
    'tasks', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('type', sa.String, nullable=False),
    sa.Column('status', sa.Integer, nullable=False),
    sa.Column('date', sa.TIMESTAMP, nullable=False),
    sa.Column('object_link', sa.String, nullable=False),
    sa.Column('amount', sa.NUMERIC, nullable=False),
    sa.Column('customer_id', sa.Integer, nullable=False)
)

tasks_to_users_table = sa.Table(
    'tasks_to_users', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('task_id', sa.Integer),
    sa.Column('user_id', sa.Integer)
)

users_table = sa.Table(
        'users', metadata,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('worker_id', sa.Integer, nullable=False),
        sa.Column('vk_id', sa.String, nullable=False),
        sa.Column('qiwi_wallet', sa.String(11), nullable=False),
)
metadata.create_all(engine)