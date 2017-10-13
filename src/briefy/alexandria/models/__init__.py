"""briefy.alexandria models."""
from briefy.alexandria.models.asset import Asset  # noQA
from briefy.alexandria.models.base import AssetsCollection  # noQA
from briefy.alexandria.models.collection import Collection  # noQA
from briefy.ws.listeners import register_workflow_context_listeners

import sqlalchemy as sa


ALL_MODELS = [
    Asset,
    AssetsCollection,
    Collection
]

# register sqlalchemy workflow context event handlers
register_workflow_context_listeners(ALL_MODELS)

sa.orm.configure_mappers()
