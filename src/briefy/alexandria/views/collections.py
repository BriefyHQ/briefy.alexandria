"""Views to handle Assets."""
from briefy.alexandria.events import collection as events
from briefy.alexandria.models import Collection
from briefy.ws import CORS_POLICY
from briefy.ws.resources import HistoryService
from briefy.ws.resources import RESTService
from briefy.ws.resources import VersionsService
from briefy.ws.resources import WorkflowAwareResource
from briefy.ws.resources.factory import BaseFactory
from cornice.resource import resource
from pyramid.security import Allow


COLLECTION_PATH = '/collections'
PATH = COLLECTION_PATH + '/{id}'


class CollectionFactory(BaseFactory):
    """Collection context factory."""

    model = Collection

    @property
    def __base_acl__(self) -> list:
        """Return ACLs in context.

        :return: list of ACLs
        :rtype: list
        """
        _acls = [
            (Allow, 'g:briefy', ['create', 'delete', 'edit', 'list', 'view'])
        ]
        return _acls


@resource(collection_path=COLLECTION_PATH,
          path=PATH,
          cors_policy=CORS_POLICY,
          factory=CollectionFactory)
class CollectionService(RESTService):
    """Collections service."""

    model = Collection
    default_order_by = 'created_at'

    _default_notify_events = {
        'POST': events.CollectionCreatedEvent,
        'PUT': events.CollectionUpdatedEvent,
        'GET': events.CollectionLoadedEvent,
        'DELETE': events.CollectionDeletedEvent,
    }

    filter_related_fields = [
        'assets'
    ]


@resource(
    collection_path=PATH + '/transitions',
    path=PATH + '/transitions/{transition_id}',
    cors_policy=CORS_POLICY,
    factory=CollectionFactory
)
class CollectionWorkflow(WorkflowAwareResource):
    """Collections workflow resource."""

    model = Collection


@resource(
    collection_path=PATH + '/versions',
    path=PATH + '/versions/{version_id}',
    cors_policy=CORS_POLICY,
    factory=CollectionFactory
)
class CollectionVersions(VersionsService):
    """Versions of Collections."""

    model = Collection


@resource(
    collection_path=PATH + '/history',
    path=PATH + '/history/{item_id}',
    cors_policy=CORS_POLICY,
    factory=CollectionFactory
)
class CollectionHistory(HistoryService):
    """Workflow history of Collections."""

    model = Collection
