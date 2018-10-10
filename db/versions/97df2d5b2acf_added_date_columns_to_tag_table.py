"""Added date columns to tag table

Revision ID: 97df2d5b2acf
Revises: 0ad10a87ca6c
Create Date: 2018-09-25 10:19:18.369622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97df2d5b2acf'
down_revision = '0ad10a87ca6c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tags', sa.Column('created_at', sa.DateTime(),
                                    server_default=sa.text('now()'), nullable=True))
    op.add_column('tags', sa.Column('updated_at', sa.DateTime(),
                                    server_default=sa.text('now()'), nullable=True))


def downgrade():
    op.drop_column('tags', 'updated_at')
    op.drop_column('tags', 'created_at')
