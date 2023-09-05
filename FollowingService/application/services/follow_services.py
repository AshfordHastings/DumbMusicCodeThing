from domain.entities.follow_entities import FollowRecord
from infrastructure.db.dbase import Session
from infrastructure.db.repository_factory import get_follow_record_repo
from infrastructure.db.exc import FollowRecordAlreadyExistsError, FollowRecordNotFoundError
from domain.services.follow import is_duplicate_follow
from domain.utils.follow_utils import FolloweeFactory, FollowerFactory

# def get_follow_status(user_id, entity_id, entity_type):
#     with Session() as session:
#         follow_record = db_ops.query_follow_record_resource(session, user_id, entity_id, entity_type)
#         if follow_record is None:
#             return False
#         else:
#             return True
#     pass

def get_follow_record_by_ids(user_id, entity_id, entity_type):
    with Session() as session:
        follow_record_repo = get_follow_record_repo(session)
        return follow_record_repo.get_by_ids(user_id, entity_id, entity_type)

def get_followers_of_entity(entity_id, entity_type, **pagination_params):
    with Session() as session:
        follow_record_repo = get_follow_record_repo(session) 
        follow_records = follow_record_repo.get_followers_of_entity(entity_id, entity_type)
        return follow_records

def get_followed_entities_by_user(user_id, entity_type, **pagination_params):
    with Session() as session:
        follow_record_repo = get_follow_record_repo(session) 
        follow_records = follow_record_repo.get_following_by_user(user_id, entity_type)
        return follow_records


def follow_entity(follower_id, followee_id, entity_type):
    follower = FollowerFactory.create("user", follower_id)
    followee = FolloweeFactory.create(entity_type, followee_id)
    follow_record = FollowRecord(follower, followee)
    # privacy_checker = MetadataServicePrivacyChecker()
    if is_duplicate_follow(follower, followee):
        raise ValueError("Duplicate follow record")
    # if is_allowed_to_follow(follower, followee, privacy_checker) and not is_duplicate_follow(follower, followee):
    #     follow_record = FollowRecord(follower, followee)
    # else:
    #     raise ValueError("Follow not allowed")
    with Session() as session:
        try:
            repo = get_follow_record_repo(session) 
            follow_record = repo.add(follow_record)
            session.commit()
        except FollowRecordAlreadyExistsError:
            raise ValueError("Duplicate follow record")
        
    return follow_record

def unfollow_entity(follower_id, followee_id, entity_type):
    with Session() as session:
        try:
            repo = get_follow_record_repo(session)
            repo.remove_by_ids(follower_id, followee_id, entity_type)
            session.commit()
        except FollowRecordNotFoundError:
            raise ValueError("Follow record not found")

def get_followers_of_entity(entity_id, entity_type, **pagination_params):
    pass


