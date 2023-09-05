
PrivacyChecker = None

class ExternalPrivacyCheck(PrivacyChecker):
    def is_private(self, entity_id: int) -> bool:
        print("Checking privacy status of entity with ID of {entity_id}.")
        return False