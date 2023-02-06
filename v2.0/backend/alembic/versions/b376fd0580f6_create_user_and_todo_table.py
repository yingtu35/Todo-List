"""create user and todo table

Revision ID: b376fd0580f6
Revises: 
Create Date: 2023-02-03 21:25:48.040531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b376fd0580f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String(30), unique=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('createdAt', sa.DateTime, default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True)
    )
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('item', sa.String, unique=True),
        sa.Column('createdAt', sa.DateTime, default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    op.drop_table('users')
    # ### end Alembic commands ###
