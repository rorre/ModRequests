"""empty message

Revision ID: 24a769ccc776
Revises: 13f56439764f
Create Date: 2020-05-30 08:47:29.259765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24a769ccc776'
down_revision = '13f56439764f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('last_updated', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_requests_last_updated'), 'requests', ['last_updated'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_requests_last_updated'), table_name='requests')
    op.drop_column('requests', 'last_updated')
    # ### end Alembic commands ###
