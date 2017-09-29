"""Collection of library items."""
from briefy.alexandria.models.mixins import LibraryItemMixin
from briefy.alexandria.db import Base
from briefy.alexandria.db import Session
from sqlalchemy.dialects.postgresql import UUID

import colander
import sqlalchemy as sa


class Collection(LibraryItemMixin, Base):
    """Collection that holds other collections or files."""

    __tablename__ = 'collections'

    __session__ = Session

    __parent_attr__ = 'parent_id'

    __raw_acl__ = (
        ('create', ('g:briefy', 'g:system')),
        ('list', ('g:briefy', 'g:system')),
        ('view', ('g:briefy', 'g:system')),
        ('edit', ('g:briefy', 'g:system')),
        ('delete', ('g:briefy', 'g:system')),
    )

    parent_id = sa.Column(
        UUID,
        sa.ForeignKey('collections.id'),
        index=True,
        nullable=True,
        info={
            'colanderalchemy': {
                'title': 'Parent',
                'validator': colander.uuid,
                'typ': colander.String,
                'missing': colander.drop
            }
        }
    )
    """Parent ID.

    Self reference foreign key :class:`briefy.alexandria.models.collection.Collection`
    """

    children = sa.orm.relationship(
        'Collection',
        foreign_keys='Collection.parent_id',
        info={
            'colanderalchemy': {
                'title': 'Parent',
                'missing': colander.drop,
            }
        }
    )
    """Children collections of this collection.

    Returns a collection of :class:`briefy.alexandria.models.collection.Collection`.
    """
