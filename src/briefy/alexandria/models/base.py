"""Base class for library items."""
from briefy.alexandria.db import Base
from briefy.alexandria.db import Session
from briefy.common.db.mixins import Timestamp
from sqlalchemy.dialects.postgresql import UUID

import colander
import sqlalchemy as sa


class AssetsCollection(Timestamp, Base):
    """Relationship between Assets and Collections."""

    __tablename__ = 'assets_collections'

    __session__ = Session

    __exclude_attributes__ = ['asset', 'collection', 'created_at', 'updated_at']

    __colanderalchemy_config__ = {
        'excludes': [
            'collection', 'asset'
        ],
    }

    asset_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey('assets.id', ondelete='CASCADE'),
        primary_key=True,
        info={
            'colanderalchemy': {
                'title': 'Asset ID',
                'validator': colander.uuid,
                'missing': colander.drop,
                'typ': colander.String
            }
        }
    )

    collection_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey('collections.id', ondelete='CASCADE'),
        primary_key=True,
        info={
            'colanderalchemy': {
                'title': 'Collection ID',
                'validator': colander.uuid,
                'missing': colander.drop,
                'typ': colander.String

            }
        }
    )

    asset = sa.orm.relationship(
        'Asset'
    )

    collection = sa.orm.relationship(
        'Collection'
    )
