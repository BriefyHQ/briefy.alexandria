"""Briefy Alexandria mixins."""
from briefy.common.db.mixins import BaseMetadata
from briefy.common.db.mixins import Mixin
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSONB

import colander
import sqlalchemy as sa


class LibraryItemMixin(BaseMetadata, Mixin):
    """Library item mixin definition."""

    source_path = sa.Column(
        sa.String(),
        nullable=False,
        index=True,
        unique=True,
        info={
            'colanderalchemy': {
                'title': 'Source Path',
                'typ': colander.String,
                'missing': '',
            }
        }
    )
    """Path to the source file in the storage.

    i.e.: files/foo/bar/image.jpg
    """

    content_type = sa.Column(
        sa.String(100),
        nullable=False,
        default='application/briefy.alexandria-collection'
    )
    """Mime type of the file.

    i.e.: image/jpeg
    """

    size = sa.Column(sa.Integer, default=0)
    """File or collection size, in bytes.

    i.e.: 4000000
    """

    tags = sa.Column(
        ARRAY(sa.String),
        default=list,
        index=True,
        info={
            'colanderalchemy': {
                'title': 'Tags',
                'typ': colander.List,
                'missing': colander.drop,
            }
        }
    )
    """List of tags to categorize item.

    i.e: ['hotel', 'room', 'berlin']
    """

    properties = sa.Column(
        JSONB,
        default=dict,
        info={
            'colanderalchemy': {
                'title': 'Properties',
                'typ': colander.Mapping,
                'missing': colander.drop,
            }
        }
    )
    """Property map to be attached to the file.

    Dictionary containing custom properties.
    """
