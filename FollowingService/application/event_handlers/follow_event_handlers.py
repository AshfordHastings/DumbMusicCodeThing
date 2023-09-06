from infrastructure.adapters.event_publishers.init_publisher import get_publisher
from domain.events.follow_events import EntityFollowedEvent

def handle_entity_follower(event:EntityFollowedEvent):
    publisher = get_publisher()
    publisher.publish(event, ['entity_follower'])
    return event