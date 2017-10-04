"""Collection of library items."""
from briefy.alexandria.models.base import AssetsCollection
from briefy.alexandria.models.mixins import LibraryItemMixin
from briefy.alexandria.db import Base
from briefy.alexandria.db import Session
from briefy.alexandria.workflows.collection import CollectionWorkflow
from briefy.ws.errors import ValidationError
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

import colander
import sqlalchemy as sa
import typing as t
import uuid


Attributes = t.List[str]


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

    __colanderalchemy_config__ = {
        'excludes': [
            'state_history', 'state', 'assets_map'
        ],
        'overrides': {
            'assets': {
                'title': 'assets',
                'missing': colander.drop,
                'typ': colander.List()
            }
        }
    }

    __exclude_attributes__ = ['assets_map']

    __summary_attributes__ = [
        'id', 'slug', 'title', 'description', 'source_path', 'content_type', 'size', 'tags'
    ]

    __to_dict_additional_attributes__ = ['assets']

    _workflow = CollectionWorkflow

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

    assets_map = sa.orm.relationship(
        'Asset',
        secondary='assets_collections',
        info={
            'colanderalchemy': {
                'title': 'Assets Collection',
                'missing': colander.drop
            }
        }
    )

    assets = association_proxy('assets_map', 'id')

    @sa.orm.validates('source_path')
    def validate_source_path(self, key: str, value: str) -> str:
        """Validate if source path is unique.

        :param key: field name
        :param value: value to be validated
        :return: value after validation
        """
        value = value if value else self.slug
        parent = self.get(self.parent_id) if self.parent_id else None
        if parent:
            value = f'{parent.source_path}/{value}'
        else:
            value = f'/{value}'
        existing = self.query().filter_by(source_path=value).one_or_none()
        if existing:
            klass_name = self.__class__.__name__
            message = f'Source path should be unique.' \
                      f'Existing {klass_name} path: {value} id: {existing.id}'
            raise ValidationError(message=message, name=key)
        return value

    @sa.orm.validates('assets_map')
    def validate_assets_map(self, key: str, value: list) -> AssetsCollection:
        """Make sure assets items are converted to instances of AssetsCollection..

        :param key: field name
        :param value: value to be validated
        :return: value after validation
        """
        from briefy.alexandria.models import Asset
        if value:
            try:
                uuid.UUID(value)
            except ValueError:
                message = f'Asset with id: "{value}" is invalid.'
                raise ValidationError(message=message, name='assets')
            value = Asset.get(value)
            if value is None:
                message = f'Asset with id: "{value}" do not exist in the database.'
                raise ValidationError(message=message, name='assets')
        return value

    @classmethod
    def create(cls, payload: dict) -> 'Base':
        """Create a new instance of this object.

        :param payload: Dictionary containing attributes and values
        :type payload: dict
        """
        source_path = payload.pop('source_path')
        assets = payload.pop('assets', [])
        id_ = payload.get('id')
        if not id_:
            payload['id'] = str(uuid.uuid4())
        obj = cls(**payload)
        obj.update({'source_path': source_path})
        session = obj.__session__
        session.add(obj)
        session.flush()
        obj.assets_map = assets
        return obj

    def to_dict(self, excludes: Attributes=None, includes: Attributes=None) -> dict:
        """Return a dictionary with fields and values used by this Class.

        :param excludes: attributes to exclude from dict representation.
        :param includes: attributes to include from dict representation.
        :returns: Dictionary with fields and values used by this Class
        """
        data = super().to_dict(excludes=excludes, includes=includes)
        data['assets'] = [item for item in self.assets if item]
        data['children'] = [item.to_summary_dict() for item in self.children if item]
        return data

    def update(self, values: dict):
        """Update the object with given values.

        :param values: Dictionary containing attributes and values
        :type values: dict
        """
        assets = values.pop('assets', None)
        for k, v in values.items():
            setattr(self, k, v)

        if assets is not None:
            self.assets_map = assets
