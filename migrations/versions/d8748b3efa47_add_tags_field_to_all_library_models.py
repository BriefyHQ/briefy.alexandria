"""add tags field to all library models.

Revision ID: d8748b3efa47
Revises: 606e588ccb3f
Create Date: 2017-10-03 16:36:37.001208
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision = 'd8748b3efa47'
down_revision = '606e588ccb3f'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database model."""
    op.add_column('assets', sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True))
    op.create_index(op.f('ix_assets_tags'), 'assets', ['tags'], unique=False)
    op.create_unique_constraint(None, 'assets', ['id'])
    op.add_column('collections', sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True))
    op.create_index(op.f('ix_collections_tags'), 'collections', ['tags'], unique=False)
    op.create_unique_constraint(None, 'collections', ['id'])


def downgrade():
    """Downgrade database model."""
    op.drop_constraint(None, 'collections', type_='unique')
    op.drop_index(op.f('ix_collections_tags'), table_name='collections')
    op.drop_column('collections', 'tags')
    op.drop_constraint(None, 'assets', type_='unique')
    op.drop_index(op.f('ix_assets_tags'), table_name='assets')
    op.drop_column('assets', 'tags')
