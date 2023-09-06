from confluent_kafka import Producer
import json

class EventPublisher:
    def publish(self, event, topics):
        raise NotImplementedError

class FauxBrokerEventPublisher(EventPublisher):
    def __init__(self, config):
        pass
    def publish(self, event, topics):
        print(f"Publishing event {type(event)} to topics {topics}")
        print(f"Event: {event}")

class KafkaEventPublisher(EventPublisher):
    def __init__(self, config):
        self.producer = Producer(config)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def publish(self, event, topics=["follow-record-created"]):
        event = json.dumps(event)
        for topic in topics:
            self.producer.produce(topic, event)
        self.producer.flush()

