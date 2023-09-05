# Only initialize the config in one module - import it from there to prevent inconsistencies
from infrastructure.db.dbase import config, Session
from infrastructure.db.repositories.sql_follow_record_repository import SQLAlchemyFollowRecordRepository

def get_follow_record_repo(session=None):
    session = session or Session()
    if config.REPOSITORY_TYPE == "SQLAlchemy":
        return SQLAlchemyFollowRecordRepository(session)
    else:
        raise Exception("Need to initialize the Repository type to generate a Repository object.")

