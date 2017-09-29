"""initial revision.

Revision ID: 606e588ccb3f
Revises: 
Create Date: 2017-09-29 17:24:09.567670
"""
import sqlalchemy as sa
from alembic import op
from briefy.common.db.types.aware_datetime import AwareDateTime
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import types

revision = '606e588ccb3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database model."""
    op.create_table('assets',
                    sa.Column('id', types.UUIDType(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('slug', sa.String(length=255), nullable=True),
                    sa.Column('created_at', AwareDateTime(), nullable=True),
                    sa.Column('state', sa.String(length=100), nullable=True),
                    sa.Column('state_history', postgresql.JSONB(astext_type=sa.Text()),
                              nullable=True),
                    sa.Column('source_path', sa.String(), nullable=False),
                    sa.Column('content_type', sa.String(length=100), nullable=False),
                    sa.Column('size', sa.Integer(), nullable=True),
                    sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('updated_at', AwareDateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_index(op.f('ix_assets_created_at'), 'assets', ['created_at'], unique=False)
    op.create_index(op.f('ix_assets_slug'), 'assets', ['slug'], unique=False)
    op.create_index(op.f('ix_assets_state'), 'assets', ['state'], unique=False)
    op.create_index(op.f('ix_assets_title'), 'assets', ['title'], unique=False)
    op.create_index(op.f('ix_assets_updated_at'), 'assets', ['updated_at'], unique=False)
    op.create_table('collections',
                    sa.Column('id', types.UUIDType(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('slug', sa.String(length=255), nullable=True),
                    sa.Column('created_at', AwareDateTime(), nullable=True),
                    sa.Column('state', sa.String(length=100), nullable=True),
                    sa.Column('state_history', postgresql.JSONB(astext_type=sa.Text()),
                              nullable=True),
                    sa.Column('source_path', sa.String(), nullable=False),
                    sa.Column('content_type', sa.String(length=100), nullable=False),
                    sa.Column('size', sa.Integer(), nullable=True),
                    sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('parent_id', postgresql.UUID(), nullable=True),
                    sa.Column('updated_at', AwareDateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['parent_id'], ['collections.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_index(op.f('ix_collections_created_at'), 'collections', ['created_at'], unique=False)
    op.create_index(op.f('ix_collections_parent_id'), 'collections', ['parent_id'], unique=False)
    op.create_index(op.f('ix_collections_slug'), 'collections', ['slug'], unique=False)
    op.create_index(op.f('ix_collections_state'), 'collections', ['state'], unique=False)
    op.create_index(op.f('ix_collections_title'), 'collections', ['title'], unique=False)
    op.create_index(op.f('ix_collections_updated_at'), 'collections', ['updated_at'], unique=False)
    op.create_table('assets_collections',
                    sa.Column('created_at', AwareDateTime(), nullable=True),
                    sa.Column('asset_id', postgresql.UUID(), nullable=False),
                    sa.Column('collection_id', postgresql.UUID(), nullable=False),
                    sa.Column('updated_at', AwareDateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
                    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
                    sa.PrimaryKeyConstraint('asset_id', 'collection_id')
                    )
    op.create_index(op.f('ix_assets_collections_created_at'), 'assets_collections', ['created_at'],
                    unique=False)
    op.create_index(op.f('ix_assets_collections_updated_at'), 'assets_collections', ['updated_at'],
                    unique=False)


def downgrade():
    """Downgrade database model."""
    op.drop_index(op.f('ix_assets_collections_updated_at'), table_name='assets_collections')
    op.drop_index(op.f('ix_assets_collections_created_at'), table_name='assets_collections')
    op.drop_table('assets_collections')
    op.drop_index(op.f('ix_collections_updated_at'), table_name='collections')
    op.drop_index(op.f('ix_collections_title'), table_name='collections')
    op.drop_index(op.f('ix_collections_state'), table_name='collections')
    op.drop_index(op.f('ix_collections_slug'), table_name='collections')
    op.drop_index(op.f('ix_collections_parent_id'), table_name='collections')
    op.drop_index(op.f('ix_collections_created_at'), table_name='collections')
    op.drop_table('collections')
    op.drop_index(op.f('ix_assets_updated_at'), table_name='assets')
    op.drop_index(op.f('ix_assets_title'), table_name='assets')
    op.drop_index(op.f('ix_assets_state'), table_name='assets')
    op.drop_index(op.f('ix_assets_slug'), table_name='assets')
    op.drop_index(op.f('ix_assets_created_at'), table_name='assets')
    op.drop_table('assets')
