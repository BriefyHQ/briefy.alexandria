"""Briefy Alexandria mixins."""
from briefy.common.db.comparator import BaseComparator
from briefy.common.db.mixins import BaseMetadata
from briefy.common.db.mixins import Mixin
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property

import colander
import sqlalchemy as sa


class LibraryTagsComparator(BaseComparator):
    """Customized comparator to filter the title from the Order."""

    def operate(self, op, other, escape=None):
        """Build the query transform function."""
        def transform(query):
            """Transform the query applying a filter."""
            values = other.split(',')
            cls = self.__clause_element__()
            filters = [cls._tags.any(value) for value in values]
            query = query.filter(sa.and_(*filters))
            return query

        return transform


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

    _tags = sa.Column(
        'tags',
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

    @hybrid_property
    def tags(self):
        """Tags getter."""
        return self._tags

    @tags.setter
    def tags(self, value: list):
        """Tags setter."""
        self._tags = value

    @tags.comparator
    def tags(cls) -> LibraryTagsComparator:
        """Tags comparator."""
        return LibraryTagsComparator(cls)

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
