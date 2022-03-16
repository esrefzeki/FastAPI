"""Testing

Revision ID: 29bc6f1ac83a
Revises: 
Create Date: 2022-03-09 09:23:41.952974+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '29bc6f1ac83a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), server_default="TRUE", nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('owner', sa.String())
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.Column('phone_number', sa.String(), nullable=True, unique=True)
                    )
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"),
                              primary_key=True),
                    sa.Column('post_id', sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"),
                              primary_key=True))

    pass


def downgrade():
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('votes')
    pass
