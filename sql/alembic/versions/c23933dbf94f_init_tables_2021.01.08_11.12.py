"""Init tables

Revision ID: c23933dbf94f
Revises: 
Create Date: 2021-01-08 11:12:31.309478

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c23933dbf94f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_queues',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('chat_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('queue',
                    sa.Column('queue_id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
                    sa.Column('notify', sa.BOOLEAN(), nullable=False),
                    sa.PrimaryKeyConstraint('queue_id'),
                    sa.UniqueConstraint('queue_id')
                    )
    op.create_table('queue_members',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('user_order', sa.Integer(), nullable=False),
                    sa.Column('current_order', sa.Integer(), nullable=False),
                    sa.Column('queue_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('user_id', 'queue_id'),
                    sa.ForeignKeyConstraint(('queue_id',), ['queue.queue_id'], ondelete='CASCADE')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('queue_members')
    op.drop_table('queue')
    op.drop_table('chat_queues')
    # ### end Alembic commands ###
