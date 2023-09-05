from domain.entities.follow_entities import FolloweeEntity, FOLLOWABLE_TYPE_REGISTRY, UserFollowerEntity

def get_followable_entity(entity_type):
    return FOLLOWABLE_TYPE_REGISTRY[entity_type]()

class FollowerFactory:
    @staticmethod
    def create(entity_type, *args, **kwargs):
        try:
            return UserFollowerEntity(*args, **kwargs)
        except KeyError:
            raise ValueError("Invalid entity type")

class FolloweeFactory:
    @staticmethod
    def create(entity_type, *args, **kwargs):
        try:
            print(f"ENTITYTYPE:{entity_type} ")
            return FOLLOWABLE_TYPE_REGISTRY[entity_type](*args, **kwargs)
        except KeyError:
            raise ValueError("Invalid entity type")
    
#get_followable_entity(entity_type):

