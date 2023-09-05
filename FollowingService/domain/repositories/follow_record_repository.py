from abc import ABC, abstractmethod

class FollowRecordRepository(ABC):
    @abstractmethod
    def get_by_id(self, follow_record_id):
        pass

    @abstractmethod
    def add(self, follow_record):
        pass