from application.event_handlers.follow_event_handlers import handle_entity_follower
from domain.events.follow_events import EntityFollowedEvent

HANDLER_CONFIG = {
    EntityFollowedEvent: [handle_entity_follower]
}