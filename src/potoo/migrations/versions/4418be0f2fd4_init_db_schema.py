"""init_db_schema

Revision ID: 4418be0f2fd4
Revises: 
Create Date: 2022-10-16 18:58:50.580313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4418be0f2fd4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow_candidates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('profiles_update_campaigns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('tweets',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('follow_campaigns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('promo_username', sa.String(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['promo_username'], ['promo_users.username'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_follow_campaigns_promo_username'), 'follow_campaigns', ['promo_username'], unique=False)
    op.create_table('followers_update_campaigns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('promo_username', sa.String(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['promo_username'], ['promo_users.username'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_followers_update_campaigns_promo_username'), 'followers_update_campaigns', ['promo_username'], unique=False)
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['profiles_update_campaigns.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_profiles_campaign_id'), 'profiles', ['campaign_id'], unique=False)
    op.create_table('follow_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requested_at', sa.DateTime(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('promo_username', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['follow_campaigns.id'], ),
    sa.ForeignKeyConstraint(['promo_username'], ['promo_users.username'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_follow_requests_campaign_id'), 'follow_requests', ['campaign_id'], unique=False)
    op.create_index(op.f('ix_follow_requests_promo_username'), 'follow_requests', ['promo_username'], unique=False)
    op.create_table('followers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('promo_username', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['followers_update_campaigns.id'], ),
    sa.ForeignKeyConstraint(['promo_username'], ['promo_users.username'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_followers_campaign_id'), 'followers', ['campaign_id'], unique=False)
    op.create_index(op.f('ix_followers_promo_username'), 'followers', ['promo_username'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_followers_promo_username'), table_name='followers')
    op.drop_index(op.f('ix_followers_campaign_id'), table_name='followers')
    op.drop_table('followers')
    op.drop_index(op.f('ix_follow_requests_promo_username'), table_name='follow_requests')
    op.drop_index(op.f('ix_follow_requests_campaign_id'), table_name='follow_requests')
    op.drop_table('follow_requests')
    op.drop_index(op.f('ix_profiles_campaign_id'), table_name='profiles')
    op.drop_table('profiles')
    op.drop_index(op.f('ix_followers_update_campaigns_promo_username'), table_name='followers_update_campaigns')
    op.drop_table('followers_update_campaigns')
    op.drop_index(op.f('ix_follow_campaigns_promo_username'), table_name='follow_campaigns')
    op.drop_table('follow_campaigns')
    op.drop_table('tweets')
    op.drop_table('profiles_update_campaigns')
    op.drop_table('follow_candidates')
    # ### end Alembic commands ###