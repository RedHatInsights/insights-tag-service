"""Added tag table

Revision ID: 0ad10a87ca6c
Revises:
Create Date: 2018-09-21 14:40:09.538252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ad10a87ca6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tags',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('value', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('tags')
