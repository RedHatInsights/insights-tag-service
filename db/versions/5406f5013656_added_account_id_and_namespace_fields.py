"""Added account_id and namespace fields

Revision ID: 5406f5013656
Revises: 97df2d5b2acf
Create Date: 2019-10-15 11:33:56.772493

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5406f5013656'
down_revision = '97df2d5b2acf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('account_id', sa.String(), nullable=True))
    op.add_column('tags', sa.Column('namespace', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'account_id')
    op.drop_column('tags', 'namespace')
    # ### end Alembic commands ###
