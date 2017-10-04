"""Asset workflow."""
from briefy.alexandria.events import asset as events
from briefy.common.workflow import WorkflowState as WS
from briefy.common.workflow import BriefyWorkflow


class AssetWorkflow(BriefyWorkflow):
    """Workflow for an Asset."""

    entity = 'asset'
    initial_state = 'created'
    update_event = events.AssetUpdatedEvent

    # States
    created = WS(
        'created', 'Created',
        'Asset created.'
    )
