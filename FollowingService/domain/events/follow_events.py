
class EntityFollowedEvent:
    def __init__(self, entity_id: str, follower_id: str, entity_type: str):
        self.entity_id = entity_id
        self.follower_id = follower_id
        self.entity_type = entity_type
    