"""initial_schema

Revision ID: 88b0cbdb246e
Revises: 
Create Date: 2026-06-17 20:36:16.154832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY


# revision identifiers, used by Alembic.
revision: str = '88b0cbdb246e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('username', sa.String(50), unique=True, nullable=True),
        sa.Column('avatar_url', sa.Text, nullable=True),
        sa.Column('role', sa.String(20), nullable=False, server_default='user'),
        sa.Column('auth_provider', sa.String(20), nullable=False, server_default='email'),
        sa.Column('google_id', sa.String(255), unique=True, nullable=True),
        sa.Column('email_verified', sa.Boolean, server_default='false'),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('household_size', sa.Integer, server_default='1'),
        sa.Column('preferences', JSONB, server_default='{}'),
        sa.Column('notification_preferences', JSONB, nullable=True),
        sa.Column('total_points', sa.Integer, server_default='0'),
        sa.Column('level', sa.Integer, server_default='1'),
        sa.Column('current_streak', sa.Integer, server_default='0'),
        sa.Column('longest_streak', sa.Integer, server_default='0'),
        sa.Column('carbon_saved_kg', sa.Integer, server_default='0'),
        sa.Column('organization_id', UUID(as_uuid=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_username', 'users', ['username'])

    # 2. Badges table
    op.create_table(
        'badges',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), unique=True, nullable=False),
        sa.Column('display_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('icon_url', sa.Text, nullable=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('rarity', sa.String(20), server_default='common'),
        sa.Column('criteria', JSONB, server_default='{}'),
        sa.Column('points_awarded', sa.Integer, server_default='50'),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_badges_category', 'badges', ['category'])

    # 3. Challenges table
    op.create_table(
        'challenges',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), unique=True, nullable=False),
        sa.Column('display_name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('challenge_type', sa.String(20), server_default='weekly'),
        sa.Column('difficulty', sa.String(20), server_default='medium'),
        sa.Column('requirements', JSONB, server_default='{}'),
        sa.Column('duration_days', sa.Integer, server_default='7'),
        sa.Column('points_reward', sa.Integer, server_default='100'),
        sa.Column('badge_reward_id', UUID(as_uuid=True), sa.ForeignKey('badges.id'), nullable=True),
        sa.Column('start_date', sa.Date, nullable=True),
        sa.Column('end_date', sa.Date, nullable=True),
        sa.Column('is_recurring', sa.Boolean, server_default='false'),
        sa.Column('participant_count', sa.Integer, server_default='0'),
        sa.Column('completion_rate', sa.Numeric(5, 2), server_default='0'),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )

    # 4. Quizzes table
    op.create_table(
        'quizzes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('difficulty', sa.String(20), server_default='beginner'),
        sa.Column('questions', JSONB, nullable=False),
        sa.Column('total_points', sa.Integer, server_default='0'),
        sa.Column('passing_score', sa.Integer, nullable=True),
        sa.Column('points_reward', sa.Integer, server_default='0'),
        sa.Column('attempt_count', sa.Integer, server_default='0'),
        sa.Column('average_score', sa.Numeric(5, 2), nullable=True),
        sa.Column('is_published', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )

    # 5. Learning Content table
    op.create_table(
        'learning_content',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), unique=True, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('difficulty', sa.String(20), server_default='beginner'),
        sa.Column('content_type', sa.String(50), nullable=False),
        sa.Column('thumbnail_url', sa.Text, nullable=True),
        sa.Column('video_url', sa.Text, nullable=True),
        sa.Column('estimated_read_time', sa.Integer, nullable=True),
        sa.Column('view_count', sa.Integer, server_default='0'),
        sa.Column('like_count', sa.Integer, server_default='0'),
        sa.Column('meta_title', sa.String(255), nullable=True),
        sa.Column('meta_description', sa.Text, nullable=True),
        sa.Column('tags', ARRAY(sa.String), server_default='{}'),
        sa.Column('is_published', sa.Boolean, server_default='false'),
        sa.Column('is_featured', sa.Boolean, server_default='false'),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('author_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_learning_slug', 'learning_content', ['slug'])

    # 6. Carbon Footprints table
    op.create_table(
        'carbon_footprints',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('monthly_kg', sa.Numeric(10, 2), nullable=False),
        sa.Column('annual_tons', sa.Numeric(10, 2), nullable=False),
        sa.Column('daily_kg', sa.Numeric(10, 2), nullable=True),
        sa.Column('grade', sa.String(20), nullable=False),
        sa.Column('grade_color', sa.String(7), nullable=True),
        sa.Column('breakdown', JSONB, nullable=False),
        sa.Column('input_data', JSONB, nullable=False),
        sa.Column('country_average_kg', sa.Numeric(10, 2), nullable=True),
        sa.Column('global_average_kg', sa.Numeric(10, 2), nullable=True),
        sa.Column('target_2c_kg', sa.Numeric(10, 2), nullable=True),
        sa.Column('insights', JSONB, server_default='[]'),
        sa.Column('calculation_method', sa.String(50), server_default='standard_v1'),
        sa.Column('ai_model', sa.String(50), server_default='claude-opus-4.5'),
        sa.Column('calculation_time_ms', sa.Integer, nullable=True),
        sa.Column('is_complete', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_carbon_user', 'carbon_footprints', ['user_id'])

    # 7. Carbon Categories table
    op.create_table(
        'carbon_categories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('footprint_id', UUID(as_uuid=True), sa.ForeignKey('carbon_footprints.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('monthly_kg', sa.Numeric(10, 2), nullable=False),
        sa.Column('percentage_of_total', sa.Numeric(5, 2), nullable=True),
        sa.Column('details', JSONB, server_default='{}'),
        sa.Column('input_data', JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_carbon_cat_footprint', 'carbon_categories', ['footprint_id'])

    # 8. Conversations table
    op.create_table(
        'conversations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('summary', sa.Text, nullable=True),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('message_count', sa.Integer, server_default='0'),
        sa.Column('context_data', JSONB, server_default='{}'),
        sa.Column('last_intent', sa.String(100), nullable=True),
        sa.Column('total_tokens_used', sa.Integer, server_default='0'),
        sa.Column('total_cost', sa.Integer, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_conv_user', 'conversations', ['user_id'])

    # 9. Messages table
    op.create_table(
        'messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', UUID(as_uuid=True), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('intent', sa.String(100), nullable=True),
        sa.Column('agent_used', sa.String(50), nullable=True),
        sa.Column('tokens_used', sa.Integer, server_default='0'),
        sa.Column('response_time_ms', sa.Integer, nullable=True),
        sa.Column('tool_calls', JSONB, server_default='[]'),
        sa.Column('rating', sa.Integer, nullable=True),
        sa.Column('feedback', sa.Text, nullable=True),
        sa.Column('metadata', JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_msg_conv', 'messages', ['conversation_id'])

    # 10. User Achievements table
    op.create_table(
        'user_achievements',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('badge_id', UUID(as_uuid=True), sa.ForeignKey('badges.id'), nullable=False),
        sa.Column('unlocked_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('progress', sa.Integer, server_default='100'),
        sa.Column('notified', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('user_id', 'badge_id', name='uq_user_badge')
    )
    op.create_index('idx_user_ach_user', 'user_achievements', ['user_id'])

    # 11. User Challenges table
    op.create_table(
        'user_challenges',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('challenge_id', UUID(as_uuid=True), sa.ForeignKey('challenges.id'), nullable=False),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('progress', JSONB, server_default='{}'),
        sa.Column('progress_percentage', sa.Integer, server_default='0'),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('points_earned', sa.Integer, server_default='0'),
        sa.Column('badge_earned', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('user_id', 'challenge_id', name='uq_user_challenge')
    )
    op.create_index('idx_user_chall_user', 'user_challenges', ['user_id'])

    # 12. Leaderboards table
    op.create_table(
        'leaderboards',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('leaderboard_type', sa.String(50), nullable=False),
        sa.Column('period', sa.String(20), nullable=False),
        sa.Column('rank', sa.Integer, nullable=False),
        sa.Column('score', sa.Numeric(10, 2), nullable=False),
        sa.Column('metric_type', sa.String(50), nullable=False),
        sa.Column('group_id', sa.String(100), nullable=True),
        sa.Column('period_start', sa.Date, nullable=False),
        sa.Column('period_end', sa.Date, nullable=False),
        sa.Column('total_participants', sa.Integer, nullable=True),
        sa.Column('percentile', sa.Numeric(5, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_leaderboard_user', 'leaderboards', ['user_id'])

    # 13. Recommendations table
    op.create_table(
        'recommendations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('detailed_steps', JSONB, server_default='[]'),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('difficulty', sa.String(20), server_default='medium'),
        sa.Column('priority_score', sa.Integer, server_default='50'),
        sa.Column('estimated_co2_savings_kg', sa.Numeric(10, 2), server_default='0'),
        sa.Column('estimated_cost_savings', sa.Numeric(10, 2), server_default='0'),
        sa.Column('estimated_time_weeks', sa.Integer, server_default='4'),
        sa.Column('impact_level', sa.String(20), server_default='medium'),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('ai_model', sa.String(50), server_default='claude-opus-4.5'),
        sa.Column('confidence_score', sa.Numeric(3, 2), server_default='0.85'),
        sa.Column('reasoning', sa.Text, nullable=True),
        sa.Column('source', sa.String(50), server_default='ai_generated'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_recommendations_user', 'recommendations', ['user_id'])

    # 14. Recommendation Actions table
    op.create_table(
        'recommendation_actions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('recommendation_id', UUID(as_uuid=True), sa.ForeignKey('recommendations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('progress_percentage', sa.Integer, server_default='0'),
        sa.Column('milestones_completed', JSONB, server_default='[]'),
        sa.Column('actual_co2_saved_kg', sa.Numeric(10, 2), nullable=True),
        sa.Column('actual_cost_impact', sa.Numeric(10, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_rec_actions_rec', 'recommendation_actions', ['recommendation_id'])

    # 15. Eco Twin States table
    op.create_table(
        'eco_twin_states',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('state_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('carbon_footprint_snapshot', JSONB, nullable=False),
        sa.Column('transportation_model', JSONB, server_default='{}'),
        sa.Column('energy_model', JSONB, server_default='{}'),
        sa.Column('food_model', JSONB, server_default='{}'),
        sa.Column('shopping_model', JSONB, server_default='{}'),
        sa.Column('waste_model', JSONB, server_default='{}'),
        sa.Column('projected_annual_tons', sa.Numeric(10, 2), nullable=True),
        sa.Column('projected_30d_kg', sa.Numeric(10, 2), nullable=True),
        sa.Column('projected_90d_kg', sa.Numeric(10, 2), nullable=True),
        sa.Column('projected_365d_kg', sa.Numeric(10, 2), nullable=True),
        sa.Column('is_baseline', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_eco_states_user', 'eco_twin_states', ['user_id'])

    # 16. Eco Twin Simulations table
    op.create_table(
        'eco_twin_simulations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('baseline_state_id', UUID(as_uuid=True), sa.ForeignKey('eco_twin_states.id'), nullable=False),
        sa.Column('simulation_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('changes_applied', JSONB, nullable=False),
        sa.Column('new_annual_tons', sa.Numeric(10, 2), nullable=False),
        sa.Column('reduction_tons', sa.Numeric(10, 2), nullable=False),
        sa.Column('reduction_percentage', sa.Numeric(5, 2), nullable=False),
        sa.Column('estimated_cost_annual', sa.Numeric(10, 2), nullable=True),
        sa.Column('savings_annual', sa.Numeric(10, 2), nullable=True),
        sa.Column('payback_period_months', sa.Integer, nullable=True),
        sa.Column('difficulty_score', sa.Integer, nullable=True),
        sa.Column('ai_recommendation_score', sa.Integer, nullable=True),
        sa.Column('ai_model', sa.String(50), server_default='claude-opus-4.5'),
        sa.Column('simulation_time_ms', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_eco_sim_user', 'eco_twin_simulations', ['user_id'])

    # 17. Quiz Attempts table
    op.create_table(
        'quiz_attempts',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('quiz_id', UUID(as_uuid=True), sa.ForeignKey('quizzes.id'), nullable=False),
        sa.Column('score', sa.Integer, nullable=False),
        sa.Column('total_possible', sa.Integer, nullable=False),
        sa.Column('percentage', sa.Numeric(5, 2), nullable=True),
        sa.Column('passed', sa.Boolean, nullable=True),
        sa.Column('answers', JSONB, nullable=False),
        sa.Column('time_taken_seconds', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_quiz_attempts_user', 'quiz_attempts', ['user_id'])

    # 18. User Analytics table
    op.create_table(
        'user_analytics',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('period_type', sa.String(20), nullable=False),
        sa.Column('period_start', sa.Date, nullable=False),
        sa.Column('period_end', sa.Date, nullable=False),
        sa.Column('login_count', sa.Integer, server_default='0'),
        sa.Column('session_duration_minutes', sa.Integer, server_default='0'),
        sa.Column('pages_viewed', sa.Integer, server_default='0'),
        sa.Column('calculations_performed', sa.Integer, server_default='0'),
        sa.Column('average_carbon_footprint', sa.Numeric(10, 2), nullable=True),
        sa.Column('carbon_reduction_pct', sa.Numeric(5, 2), nullable=True),
        sa.Column('ai_conversations', sa.Integer, server_default='0'),
        sa.Column('ai_messages_sent', sa.Integer, server_default='0'),
        sa.Column('points_earned', sa.Integer, server_default='0'),
        sa.Column('badges_unlocked', sa.Integer, server_default='0'),
        sa.Column('challenges_completed', sa.Integer, server_default='0'),
        sa.Column('articles_read', sa.Integer, server_default='0'),
        sa.Column('quizzes_taken', sa.Integer, server_default='0'),
        sa.Column('recommendations_received', sa.Integer, server_default='0'),
        sa.Column('recommendations_accepted', sa.Integer, server_default='0'),
        sa.Column('recommendations_completed', sa.Integer, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_analytics_user', 'user_analytics', ['user_id'])

    # 19. Audit Logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('actor_type', sa.String(50), nullable=False),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('resource_id', UUID(as_uuid=True), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('changes', JSONB, nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text, nullable=True),
        sa.Column('status', sa.String(20), server_default='success'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )


def downgrade() -> None:
    # Drop in reverse dependency order
    op.drop_table('audit_logs')
    op.drop_table('user_analytics')
    op.drop_table('quiz_attempts')
    op.drop_table('eco_twin_simulations')
    op.drop_table('eco_twin_states')
    op.drop_table('recommendation_actions')
    op.drop_table('recommendations')
    op.drop_table('leaderboards')
    op.drop_table('user_challenges')
    op.drop_table('user_achievements')
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('carbon_categories')
    op.drop_table('carbon_footprints')
    op.drop_table('learning_content')
    op.drop_table('quizzes')
    op.drop_table('challenges')
    op.drop_table('badges')
    op.drop_table('users')
