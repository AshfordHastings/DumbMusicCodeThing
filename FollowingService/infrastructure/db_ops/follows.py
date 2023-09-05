
from sqlalchemy.orm import sessionmaker, scoped_session

from domain.model import FollowRecord

DB_SESSION = scoped_session(sessionmaker(bind=DB_ENGINE))

def query_follow_record_resource_by_id(follow_record_id):
    session = DB_SESSION()
    return session.query(FollowRecord).filter(FollowRecord.followRecordId == follow_record_id).first()

def query_follow_record_resource(session, follower_id, followee_id, followed_type):
    return session.query(FollowRecord).filter(FollowRecord.followerId == follower_id).filter(FollowRecord.followeeId == followee_id).filter(FollowRecord.followed_type == followed_type).first()

def query_follow_record_list(session, follower_id, followed_type=None):
    if followed_type is None:
        return session.query(FollowRecord).filter(FollowRecord.followerId == follower_id).all()
    else:
        return session.query(FollowRecord).filter(FollowRecord.followerId == follower_id).filter(FollowRecord.followed_type == followed_type).all()
    
def query_followed_record_list(session, followee_id, followed_type=None):
    if followed_type is None:
        return session.query(FollowRecord).filter(FollowRecord.followeeId == followee_id).all()
    else:
        return session.query(FollowRecord).filter(FollowRecord.followeeId == followee_id).filter(FollowRecord.followed_type == followed_type).all()
    
def insert_follow_record(session, follow_record):
    session.add(follow_record)
    session.commit()
    return follow_record

def insert_follow_record_resource(session, follower_id, followee_id, followed_type):
    follow_record = FollowRecord(followerId=follower_id, followeeId=followee_id, followed_type=followed_type)
    session.add(follow_record)
    session.commit()
    return follow_record

def delete_follow_record(session, follow_record):
    session.delete(follow_record)
    session.commit()
    return follow_record