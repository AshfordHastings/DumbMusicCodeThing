
from infrastructure.db.dbase import Session



def get_follow_status(user_id, entity_id, entity_type):
    with Session():
        
        follow_record = db_ops.query_follow_record_resource(session, user_id, entity_id, entity_type)
        if follow_record is None:
            return False
        else:
            return True

def is_allowed_to_follow(follower, followee, privacy_checker):
    pass

def is_duplicate_follow(follower, followee):
    return False