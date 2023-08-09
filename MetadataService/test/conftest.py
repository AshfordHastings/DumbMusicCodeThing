import pytest 
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from api.app import create_app
from domain import Base
from .db_scripts.insert_artist_data import insert_artist_data

@pytest.fixture()
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture()
def session_factory(in_memory_db):
    yield sessionmaker(bind=in_memory_db)

@pytest.fixture()
def client(session_factory):
    app = create_app(session_factory)
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture()
def populate_artist_data(in_memory_db):
    with open('sql_scripts/insert_artist_data.sql') as f:
        raw_data = f.read()
    statements = raw_data.split(';')
    with in_memory_db.connect() as conn:
        for statement in statements:
            stmt = text(statement)
            conn.execute(stmt)
        conn.commit()
    return 

@pytest.fixture()
def populate_song_data(in_memory_db, populate_artist_data):
    with open('sql_scripts/insert_song_data.sql') as f:
        raw_data = f.read()
    statements = raw_data.split(';')
    with in_memory_db.connect() as conn:
        for statement in statements:
            stmt = text(statement)
            conn.execute(stmt)
        conn.commit()
    return 


@pytest.fixture()
def populate_empty_playlist_data(in_memory_db):
    with open('sql_scripts/insert_playlist_data.sql') as f:
        raw_data = f.read()
    statements = raw_data.split(';')
    with in_memory_db.connect() as conn:
        for statement in statements:
            stmt = text(statement)
            conn.execute(stmt)
        conn.commit()
    return 

@pytest.fixture()
def populate_playlist_data(in_memory_db, populate_empty_playlist_data, populate_song_data):
    with open('sql_scripts/insert_playlist_association_data.sql') as f:
        raw_data = f.read()
    statements = raw_data.split(';')
    with in_memory_db.connect() as conn:
        for statement in statements:
            stmt = text(statement)
            conn.execute(stmt)
        conn.commit()
    return 


#INSERT INTO playlists_to_songs (playlistId, songId) VALUES ((SELECT playlistId FROM playlists WHERE name=""), (SELECT songId FROM songs WHERE title=""));