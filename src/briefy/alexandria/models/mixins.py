"""Briefy Alexandria mixins."""
from briefy.common.db.mixins import BaseMetadata
from briefy.common.db.mixins import Mixin
from sqlalchemy.dialects.postgresql import JSONB

import colander
import sqlalchemy as sa


class LibraryItemMixin(BaseMetadata, Mixin):
    """Library item mixin definition."""

    source_path = sa.Column(sa.String(), nullable=False)
    """Path to the source file in the storage.

    i.e.: files/foo/bar/image.jpg
    """

    content_type = sa.Column(sa.String(100), nullable=False)
    """Mime type of the file.

    i.e.: image/jpeg
    """

    size = sa.Column(sa.Integer, default=0)
    """File or collection size, in bytes.

    i.e.: 4000000
    """

    properties = sa.Column(
        JSONB,
        info={
            'colanderalchemy': {
                'title': 'Requirement Items',
                'typ': colander.Mapping,
                'missing': colander.drop,
            }
        }
    )
    """Property map to be attached to the file.

    Dictionary containing custom properties.
    """
