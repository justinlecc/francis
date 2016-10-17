"""empty message

Revision ID: 6ae32ca83575
Revises: None
Create Date: 2016-10-16 21:44:27.091337

"""

# revision identifiers, used by Alembic.
revision = '6ae32ca83575'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('humans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('nickname', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_humans_phone_number'), 'humans', ['phone_number'], unique=True)
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('human_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['human_id'], ['humans.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_index(op.f('ix_humans_phone_number'), table_name='humans')
    op.drop_table('humans')
    ### end Alembic commands ###