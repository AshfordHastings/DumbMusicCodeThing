import pytest 
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker

from api.app import create_app
from domain import Base
from utils.auth import encode_auth_token
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

@pytest.fixture()
def populate_user_data(in_memory_db):
    users = [
        {"username": "admin", "password": generate_password_hash("adminpass"), "email": "admin@example.com"},
        {"username": "user1", "password": generate_password_hash("user1pass"), "email": "user1@example.com"},
        # ... Add more users as needed
    ]

    with in_memory_db.connect() as conn:
        for user in users:
            stmt = text(f"INSERT INTO users (username, password, email) VALUES (:username, :password, :email)")
            conn.execute(stmt, **user)
        conn.commit()

    return

@pytest.fixture()
def populate_roles_data(in_memory_db):
    roles = ["admin", "editor", "user"]
    
    with in_memory_db.connect() as conn:
        for role in roles:
            stmt = text(f"INSERT INTO roles (roleName) VALUES (:role_name)")
            conn.execute(stmt, {'role_name': role})
        conn.commit()

    return

@pytest.fixture()
def populate_user_roles_data(in_memory_db, populate_user_data, populate_roles_data):
    user_roles = [
        {"username": "admin", "role": "admin"},
        {"username": "user1", "role": "user"},
        # ... Add more associations as needed
    ]

    with in_memory_db.connect() as conn:
        for ur in user_roles:
            stmt = text("""
                INSERT INTO user_roles (user_id, role_id) 
                VALUES (
                    (SELECT id FROM users WHERE username=:username), 
                    (SELECT id FROM roles WHERE roleName=:role)
                )
            """)
            conn.execute(stmt, **ur)
        conn.commit()

    return

@pytest.fixture()
def test_user(in_memory_db):
    user_data = {
        "username": "testuser",
        "password": generate_password_hash("testpassword"),  # Assuming you have hash_password function as shown before
        "email": "testuser@example.com",
        'displayName': 'Test User'
    }

    with in_memory_db.connect() as conn:
        stmt = text("INSERT INTO users (username, password, email, displayName) VALUES (:username, :password, :email, :displayName)")
        result = conn.execute(stmt, user_data)
        user_data["userId"] = result.lastrowid
        conn.commit()

    return user_data

@pytest.fixture()
def test_admin(in_memory_db):
    user_data = {
        "username": "testadmin",
        "password": generate_password_hash("testpassword"),  # Assuming you have hash_password function as shown before
        "email": "testadmin@example.com",
        'displayName': 'Test Admin'
    }

    with in_memory_db.connect() as conn:
        stmt = text("INSERT INTO users (username, password, email, displayName) VALUES (:username, :password, :email, :displayName)")
        result = conn.execute(stmt, user_data)
        user_data["userId"] = result.lastrowid
        conn.commit()

    return user_data

@pytest.fixture()
def test_admin_jwt(test_user, populate_roles_data):
    return encode_auth_token(test_user['userId'], roles=['admin', 'user'])

@pytest.fixture()
def test_user_jwt(test_user, populate_roles_data):
    return encode_auth_token(test_user['userId'], roles=['user'])



#INSERT INTO playlists_to_songs (playlistId, songId) VALUES ((SELECT playlistId FROM playlists WHERE name=""), (SELECT songId FROM songs WHERE title=""));