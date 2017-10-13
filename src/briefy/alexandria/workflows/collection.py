"""Collection workflow."""
from briefy.alexandria.events import collection as events
from briefy.common.workflow import WorkflowState as WS
from briefy.common.workflow import BriefyWorkflow


class CollectionWorkflow(BriefyWorkflow):
    """Workflow for a Collection."""

    entity = 'collection'
    initial_state = 'created'
    update_event = events.CollectionUpdatedEvent

    # States
    created = WS(
        'created', 'Created',
        'Collection created.'
    )
