"""Add SustainabilityReport and ai_sustainability_score

Revision ID: fd60a81f2e09
Revises: 88b0cbdb246e
Create Date: 2026-06-17 21:11:12.947152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd60a81f2e09'
down_revision: Union[str, None] = '88b0cbdb246e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add visualization_data to recommendations
    op.add_column('recommendations', sa.Column('visualization_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    # Add ai_sustainability_score to carbon_footprints
    op.add_column('carbon_footprints', sa.Column('ai_sustainability_score', sa.Integer(), nullable=True))

    # Create sustainability_reports table
    op.create_table('sustainability_reports',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('report_type', sa.String(length=20), nullable=True),
    sa.Column('period_start', sa.Date(), nullable=False),
    sa.Column('period_end', sa.Date(), nullable=False),
    sa.Column('summary_text', sa.Text(), nullable=False),
    sa.Column('key_insights', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('carbon_saved_kg', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('points_earned', sa.Integer(), nullable=True),
    sa.Column('challenges_completed', sa.Integer(), nullable=True),
    sa.Column('ai_sustainability_score', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sustainability_reports_user_id'), 'sustainability_reports', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_sustainability_reports_user_id'), table_name='sustainability_reports')
    op.drop_table('sustainability_reports')
    op.drop_column('carbon_footprints', 'ai_sustainability_score')
    op.drop_column('recommendations', 'visualization_data')
