"""add createdAt for User

Revision ID: 6a89954f982f
Revises: 
Create Date: 2023-01-30 19:36:00.742598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a89954f982f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('createdAt', sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'createdAt')
