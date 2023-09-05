import pytest

from application.services import follow_services
from infrastructure.db.dbase import init_db, teardown_db, close_db

@pytest.fixture(scope='function', autouse=True)
def dev_db():
    yield init_db()
    teardown_db()
    close_db()

@pytest.fixture()
def extant_follow_record():
    follow_record = follow_services.follow_entity(1, 1, "playlist")
    yield follow_record

@pytest.fixture()
def extant_user_follows_many_records(dev_db):
    yield [follow_services.follow_entity(1, i, "playlist") for i in range(1, 10)]


#@pytest.mark.usefixtures('dev_db')
@pytest.mark.skip(reason="Testing successful.")
def test_follow_playlist_entity():
    follow_record = follow_services.follow_entity(1, 1, "playlist")
    assert follow_record 
    assert follow_record.follower.id == 1
    assert follow_record.followee.id == 1
    assert follow_record.followee_type == "playlist"

@pytest.mark.skip(reason="Testing successful.")
def test_unfollow_playlist_entity(extant_follow_record):
    follow_services.unfollow_entity(extant_follow_record.follower.id, extant_follow_record.followee.id, extant_follow_record.followee_type)
    assert not follow_services.get_follow_record_by_ids(extant_follow_record.follower.id, extant_follow_record.followee.id, extant_follow_record.followee_type)

def test_user_follows_many_records(extant_user_follows_many_records):
    follow_records = follow_services.get_followed_entities_by_user(1, "playlist")
    assert len(follow_records) == len(extant_user_follows_many_records)
    assert follow_records[0].follower.id == 1
