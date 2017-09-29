"""Custom briefy.alexandria events for model Collection."""
from briefy.alexandria import logger
from briefy.ws.resources import events


class CollectionCreatedEvent(events.ObjectCreatedEvent):
    """Event to notify collection creation."""

    event_name = 'collection.created'
    logger = logger


class CollectionUpdatedEvent(events.ObjectUpdatedEvent):
    """Event to notify collection update."""

    event_name = 'collection.updated'
    logger = logger


class CollectionDeletedEvent(events.ObjectDeletedEvent):
    """Event to notify collection delete."""


class CollectionLoadedEvent(events.ObjectLoadedEvent):
    """Event to notify collection load."""
