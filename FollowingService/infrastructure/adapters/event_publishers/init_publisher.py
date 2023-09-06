from config import get_config
from infrastructure.adapters.event_publishers.publishers import KafkaEventPublisher, FauxBrokerEventPublisher

_publisher_instance = None

def get_publisher():
    global _publisher_instance
    if _publisher_instance is None:
        _publisher_instance = init_publisher()
    return _publisher_instance

def init_publisher():
    global _publisher_instance
    if _publisher_instance is None:
        config = get_config()
        if config.EVENT_PUBLISHER == "kafka":
            _publisher_instance = KafkaEventPublisher(config.KAFKA_CONFIG)
        elif config.EVENT_PUBLISHER == "faux-broker":
            _publisher_instance = FauxBrokerEventPublisher({})
        else:
            raise ValueError("Invalid event publisher")
    return _publisher_instance

def close_publisher():
    global _publisher_instance
    if _publisher_instance is not None:
        _publisher_instance.close()
        _publisher_instance = None