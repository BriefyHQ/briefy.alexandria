"""Views to handle Assets."""
from briefy.alexandria.events import asset as events
from briefy.alexandria.models import Asset
from briefy.ws import CORS_POLICY
from briefy.ws.resources import HistoryService
from briefy.ws.resources import RESTService
from briefy.ws.resources import VersionsService
from briefy.ws.resources import WorkflowAwareResource
from briefy.ws.resources.factory import BaseFactory
from cornice.resource import resource
from pyramid.security import Allow


COLLECTION_PATH = '/assets'
PATH = COLLECTION_PATH + '/{id}'


class AssetFactory(BaseFactory):
    """Asset context factory."""

    model = Asset

    @property
    def __base_acl__(self) -> list:
        """Return ACLs in context.

        :return: list of ACLs
        :rtype: list
        """
        _acls = [
            (Allow, 'g:briefy', ['create', 'list', 'view', 'edit', 'delete'])
        ]
        return _acls


@resource(collection_path=COLLECTION_PATH,
          path=PATH,
          cors_policy=CORS_POLICY,
          factory=AssetFactory)
class AssetService(RESTService):
    """Assets service."""

    model = Asset
    default_order_by = 'created_at'

    _default_notify_events = {
        'POST': events.AssetCreatedEvent,
        'PUT': events.AssetUpdatedEvent,
        'GET': events.AssetLoadedEvent,
        'DELETE': events.AssetDeletedEvent,
    }

    filter_related_fields = [
        'collections'
    ]


@resource(
    collection_path=PATH + '/transitions',
    path=PATH + '/transitions/{transition_id}',
    cors_policy=CORS_POLICY,
    factory=AssetFactory
)
class AssetWorkflow(WorkflowAwareResource):
    """Assets workflow resource."""

    model = Asset


@resource(
    collection_path=PATH + '/versions',
    path=PATH + '/versions/{version_id}',
    cors_policy=CORS_POLICY,
    factory=AssetFactory
)
class AssetVersions(VersionsService):
    """Versions of assets."""

    model = Asset


@resource(
    collection_path=PATH + '/history',
    path=PATH + '/history/{item_id}',
    cors_policy=CORS_POLICY,
    factory=AssetFactory
)
class AssetHistory(HistoryService):
    """Workflow history of assets."""

    model = Asset
