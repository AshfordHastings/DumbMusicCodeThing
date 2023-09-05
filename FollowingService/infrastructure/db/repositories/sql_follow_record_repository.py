from sqlalchemy.exc import IntegrityError

from domain.repositories.follow_record_repository import FollowRecordRepository
from domain.entities.follow_entities import FollowRecord
from infrastructure.db.models.follow import FollowRecordModel, FollowedType
from infrastructure.db.exc import FollowRecordAlreadyExistsError, FollowRecordNotFoundError
from domain.utils.follow_utils import FolloweeFactory, FollowerFactory
from typing import List

class SQLAlchemyFollowRecordRepository(FollowRecordRepository):
    def __init__(self, session):
        self.session = session

    def add(self, follow_record: FollowRecord):
        model = self._to_data_model(follow_record)
        try:
            self.session.add(model)
            self.session.flush()
            return self._to_domain_entity(model)
        except IntegrityError:
            raise FollowRecordAlreadyExistsError(f"A follow record for follower_id {follow_record.follower.id} and followee_id {follow_record.followee.id} already exists.") from None
    
    # def remove(self, follow_record: FollowRecord):
    #     model = self._to_data_model(follow_record)
    #     try:
    #     self.session.delete(model)
    #     self.session.flush()
    #     return model.id

    def get_by_ids(self, follower_id: int, followee_id: int, entity_type: str) -> FollowRecord:
        model = self.session.query(FollowRecordModel).filter_by(followerId=follower_id, followeeId=followee_id, followed_type=entity_type).first()
        return self._to_domain_entity(model) if model else None

    def remove_by_ids(self, follower_id: int, followee_id: int, entity_type: str) -> None:
        #TODO: Make a schema, or something, that allows me to query.
        model = self.session.query(FollowRecordModel).filter_by(followerId=follower_id, followeeId=followee_id, followed_type=entity_type).first()
        if model:
            self.session.delete(model)
            self.session.flush()
        else:
            raise FollowRecordNotFoundError(f"Follow record for follower_id {follower_id} and followee_id {followee_id} not found.")


    def get_by_id(self, follow_record_id):
        model = self.session.query(FollowRecord).filter(FollowRecord.followRecordId == follow_record_id).first()
        model = self._to_domain_entity(model) if model else None

    def get_followers_of_entity(self, entity_id: int, entity_type: str) -> List[FollowRecord]:
        models = self.session.query(FollowRecordModel).filter_by(followed_id=entity_id, followed_type=entity_type).all()
        return [self._to_domain_entity(model) for model in models]

    def get_following_by_user(self, user_id: int, entity_type: str) -> List[FollowRecord]:
        models = self.session.query(FollowRecordModel).filter_by(followerId=user_id, followed_type=entity_type).all()
        return [self._to_domain_entity(model) for model in models]

    def count_followers_of_entity(self, entity_id: int, entity_type: str) -> int:
        return self.session.query(FollowRecordModel).filter_by(followerId=entity_id, followed_type=entity_type).count()

    def count_following_by_user(self, user_id: int) -> int:
        return self.session.query(FollowRecordModel).filter_by(followerId=user_id).count()
    
    def _to_domain_entity(self, model:FollowRecordModel) -> FollowRecord:
        follower = FollowerFactory.create("user", model.followerId)
        followed_type_value = model.followed_type.value if isinstance(model.followed_type, FollowedType) else model.followed_type
        followee = FolloweeFactory.create(followed_type_value, model.followeeId)
        return FollowRecord(follower, followee)
    
    def _to_data_model(self, follow_record: FollowRecord):
        return FollowRecordModel(followerId=follow_record.follower.id, followeeId=follow_record.followee.id, followed_type=follow_record.followee.type)