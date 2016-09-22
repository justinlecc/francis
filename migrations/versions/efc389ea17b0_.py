"""empty message

Revision ID: efc389ea17b0
Revises: 550373caff24
Create Date: 2016-09-21 08:09:22.506940

"""

# revision identifiers, used by Alembic.
revision = 'efc389ea17b0'
down_revision = '550373caff24'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('nickname', sa.String(length=20), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'nickname')
    ### end Alembic commands ###
