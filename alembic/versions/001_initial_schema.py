"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-06-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create work_sessions table
    op.create_table(
        'work_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login_time', sa.DateTime(), nullable=False),
        sa.Column('logout_time', sa.DateTime(), nullable=True),
        sa.Column('logout_type', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create settings table
    op.create_table(
        'settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=100), nullable=False),
        sa.Column('value', sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    
    # Insert default settings
    op.execute(
        "INSERT INTO settings (key, value) VALUES ('week_start_day', '0')"  # 0 = Monday
    )

def downgrade() -> None:
    op.drop_table('settings')
    op.drop_table('work_sessions')