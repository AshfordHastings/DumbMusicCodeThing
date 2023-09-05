from abc import ABC, abstractmethod

class PrivacyChecker(ABC):
    @abstractmethod
    def is_private(self, entity_id: int) -> bool:
        pass