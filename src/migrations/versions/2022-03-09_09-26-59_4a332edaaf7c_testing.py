"""Testing

Revision ID: 4a332edaaf7c
Revises: 29bc6f1ac83a
Create Date: 2022-03-09 09:26:59.831242+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4a332edaaf7c'
down_revision = '29bc6f1ac83a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
                  sa.Column('phone_number', sa.String(), nullable=True, unique=True))
    pass


def downgrade():
    op.drop_column('users', 'phone_number')
    pass
