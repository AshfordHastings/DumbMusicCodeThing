from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#DATABASE_URI = "sqlite:////Users/ashfordhastings/PythonProjects/Practice Projects/prac-29-speed-api-1/dev.db"
DATABASE_URI = "postgresql://postgres:password@localhost:5432/metadata_db"

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()