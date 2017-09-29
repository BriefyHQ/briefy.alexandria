"""Asset definition."""
from briefy.alexandria.models.mixins import LibraryItemMixin
from briefy.alexandria.db import Base
from briefy.alexandria.db import Session


class Asset(LibraryItemMixin, Base):
    """Asset is a base class for any file we will have in the library.
    """

    __tablename__ = 'assets'

    __session__ = Session

    __raw_acl__ = (
        ('create', ('g:briefy', 'g:system')),
        ('list', ('g:briefy', 'g:system')),
        ('view', ('g:briefy', 'g:system')),
        ('edit', ('g:briefy', 'g:system')),
        ('delete', ('g:briefy', 'g:system')),
    )
