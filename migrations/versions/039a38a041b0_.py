"""empty message

Revision ID: 039a38a041b0
Revises: da970f8a5a98
Create Date: 2025-07-15 20:45:06.500370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '039a38a041b0'
down_revision = 'da970f8a5a98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('toke_blocked_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('toke_blocked_list')
    # ### end Alembic commands ###
