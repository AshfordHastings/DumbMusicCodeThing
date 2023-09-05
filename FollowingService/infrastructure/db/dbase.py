from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import get_config
from infrastructure.db.models import Base

config = get_config()

engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
Session = scoped_session(sessionmaker(bind=engine))


def init_db():
    Base.metadata.create_all(engine)

def close_db():
    engine.dispose()

def teardown_db():
    Base.metadata.drop_all(engine)