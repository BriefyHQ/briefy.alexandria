"""Custom briefy.alexandria events for model Asset."""
from briefy.alexandria import logger
from briefy.ws.resources import events


class AssetCreatedEvent(events.ObjectCreatedEvent):
    """Event to notify asset creation."""

    event_name = 'asset.created'
    logger = logger


class AssetUpdatedEvent(events.ObjectUpdatedEvent):
    """Event to notify asset update."""

    event_name = 'asset.updated'
    logger = logger


class AssetDeletedEvent(events.ObjectDeletedEvent):
    """Event to notify asset delete."""


class AssetLoadedEvent(events.ObjectLoadedEvent):
    """Event to notify asset load."""
