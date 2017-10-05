"""add base collections.

Revision ID: 2f242e8a4a21
Revises: d8748b3efa47
Create Date: 2017-10-05 12:07:04.720095
"""
from alembic import op

revision = '2f242e8a4a21'
down_revision = 'd8748b3efa47'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database model."""
    op.execute('''
    INSERT INTO collections 
    (id, title, description, slug, created_at, state, 
     state_history, source_path, content_type, updated_at, tags)
     
    VALUES
    (
        '48f47fdc-922b-4aae-8388-0fb23a123fcc',
        'Leica',
        'Leica root collection.',
        'Leica',
        current_timestamp,
        'created',
        JSONB('[{"to": "created", "date": "2017-10-05T10:19:57.296475+00:00", "from": "", 
          "actor": "", "message": "", "transition": "create"}]'),
        '/Leica',
        'application/collection.leica-root',
        current_timestamp,
        ARRAY['leica', 'root', 'application']
    ),
    (
        '27f0cdff-14da-42c4-880a-51c3d6f0b841',
        'City Packages',
        'City Packages root collection.',
        'City-Packages',
        current_timestamp,
        'created',
        JSONB('[{"to": "created", "date": "2017-10-05T10:19:57.296475+00:00", "from": "", 
          "actor": "", "message": "", "transition": "create"}]'),
        '/City-Packages',
        'application/collection.citypackages-root',
        current_timestamp,
        ARRAY['citypackages', 'root', 'application']
    )
    ''')


def downgrade():
    """Downgrade database model."""
    op.execute('''
    DELETE from collections where id IN (
        '48f47fdc-922b-4aae-8388-0fb23a123fcc',
        '27f0cdff-14da-42c4-880a-51c3d6f0b841'
    )
    ''')
