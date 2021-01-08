"""created chat table, deleted chat_queues

Revision ID: bae3d4951627
Revises: c23933dbf94f
Create Date: 2021-01-08 14:50:10.778245

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'bae3d4951627'
down_revision = 'c23933dbf94f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_queues')

    op.create_table('chat',
                    sa.Column('chat_id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
                    sa.PrimaryKeyConstraint('chat_id', name='chat_id_pkey'),
                    sa.UniqueConstraint('chat_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_queues',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('chat_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='chat_queues_pkey')
                    )

    op.drop_table('chat')
    # ### end Alembic commands ###
