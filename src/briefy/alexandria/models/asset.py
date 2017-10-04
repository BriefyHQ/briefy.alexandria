"""Asset definition."""
from briefy.alexandria.models.base import AssetsCollection
from briefy.alexandria.models.mixins import LibraryItemMixin
from briefy.alexandria.db import Base
from briefy.alexandria.db import Session
from briefy.alexandria.workflows.asset import AssetWorkflow
from briefy.ws.errors import ValidationError
from sqlalchemy.ext.associationproxy import association_proxy

import colander
import sqlalchemy as sa
import typing as t
import uuid


Attributes = t.List[str]

DEFAULT_BUCKET = '/assets'


class Asset(LibraryItemMixin, Base):
    """Asset is a base class for any file we will have in the library."""

    __tablename__ = 'assets'

    __session__ = Session

    __raw_acl__ = (
        ('create', ('g:briefy', 'g:system')),
        ('list', ('g:briefy', 'g:system')),
        ('view', ('g:briefy', 'g:system')),
        ('edit', ('g:briefy', 'g:system')),
        ('delete', ('g:briefy', 'g:system')),
    )

    __summary_attributes__ = [
        'id', 'slug', 'title', 'description', 'source_path', 'content_type', 'size', 'tags'
    ]

    __exclude_attributes__ = ['collections_map']

    __colanderalchemy_config__ = {
        'excludes': [
            'state_history', 'state', 'collections_map'
        ],
        'overrides': {
            'collections': {
                'title': 'Collections',
                'missing': colander.drop,
                'typ': colander.List()
            }
        }
    }

    _workflow = AssetWorkflow

    collections_map = sa.orm.relationship(
        'Collection',
        secondary='assets_collections',
        info={
            'colanderalchemy': {
                'title': 'Collections Asset',
                'missing': colander.drop
            }
        }
    )

    collections = association_proxy('collections_map', 'id')

    @sa.orm.validates('source_path')
    def validate_source_path(self, key: str, value: str) -> str:
        """Validate if source path is unique.

        :param key: field name
        :param value: value to be validated
        :return: value after validation
        """
        value = value if value else str(self.id)
        existing = self.query().filter_by(source_path=value).one_or_none()
        if existing:
            klass_name = self.__class__.__name__
            message = f'Source path should be unique.' \
                      f'Existing {klass_name} path: {value} id: {existing.id}'
            raise ValidationError(message=message, name=key)
        return f'{DEFAULT_BUCKET}/{value}'

    @sa.orm.validates('collections_map')
    def validate_collections_map(self, key: str, value: list) -> AssetsCollection:
        """Make sure collections items are converted to instances of AssetsCollection.

        :param key: field name
        :param value: value to be validated
        :return: value after validation
        """
        from briefy.alexandria.models import Collection
        if value:
            try:
                uuid.UUID(value)
            except ValueError:
                message = f'Collection with id: "{value}" is invalid.'
                raise ValidationError(message=message, name='collections')
            value = Collection.get(value)
            if value is None:
                message = f'Collection with id: "{value}" do not exist in the database.'
                raise ValidationError(message=message, name='collections')
        return value

    @classmethod
    def create(cls, payload: dict) -> 'Base':
        """Create a new instance of this object.

        :param payload: Dictionary containing attributes and values
        :type payload: dict
        """
        source_path = payload.pop('source_path', '')
        collections = payload.pop('collections', [])
        id_ = payload.get('id')
        if not id_:
            payload['id'] = str(uuid.uuid4())
        obj = cls(**payload)
        obj.update({'source_path': source_path})
        session = obj.__session__
        session.add(obj)
        session.flush()
        obj.collections_map = collections
        return obj

    def to_dict(self, excludes: Attributes=None, includes: Attributes=None) -> dict:
        """Return a dictionary with fields and values used by this Class.

        :param excludes: attributes to exclude from dict representation.
        :param includes: attributes to include from dict representation.
        :returns: Dictionary with fields and values used by this Class
        """
        data = super().to_dict(excludes=excludes, includes=includes)
        data['collections'] = [item for item in self.collections if item]
        return data

    def update(self, values: dict):
        """Update the object with given values.

        :param values: Dictionary containing attributes and values
        :type values: dict
        """
        collections = values.pop('collections', None)
        for k, v in values.items():
            setattr(self, k, v)

        if collections is not None:
            self.collections_map = collections
