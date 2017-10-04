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

    asset_id = sa.Column(
        UUID,
        sa.ForeignKey('assets.id'),
        primary_key=True,
        info={
            'colanderalchemy': {
                'title': 'Asset ID',
                'validator': colander.uuid,
                'typ': colander.String
            }
        }
    )

    collection_id = sa.Column(
        UUID,
        sa.ForeignKey('collections.id'),
        primary_key=True,
        info={
            'colanderalchemy': {
                'title': 'Collection ID',
                'validator': colander.uuid,
                'typ': colander.String

            }
        }
    )

    asset = sa.orm.relationship(
        'Asset',
        backref='collections'
    )

    collection = sa.orm.relationship(
        'Collection',
        backref='assets'
    )
