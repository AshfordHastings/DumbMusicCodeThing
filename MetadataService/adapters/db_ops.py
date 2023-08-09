from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from domain.model import Song, Artist, Playlist, User, PlaylistSongAssociation
from exc import ResourceNotFound

def query_song_list(session):
    resp_song_list = session.query(Song).all()
    return resp_song_list

def query_song_resource(session, song_id):
    resp_song_resource = session.query(Song).filter_by(songId=song_id).first()
    if resp_song_resource is None:
        raise ResourceNotFound(f"Song resource with id of {song_id} is not found.")
    return resp_song_resource

def insert_song_resource(session, data):
    session.add(data)
    session.flush()
    return data

def delete_song_resource(session, song_id):
    resp_song_resource = session.query(Song).filter_by(artistId=song_id).first()
    if resp_song_resource:
        session.delete(resp_song_resource)
        session.flush()
    else:
        raise ResourceNotFound(f"Artist resource with id of {song_id} is not found.")

def query_artist_list(session):
    resp_artist_list = session.query(Artist).all()
    return resp_artist_list

def query_artist_resource(session, artist_id):
    resp_artist_resource = session.query(Artist).filter_by(artistId=artist_id).first()
    if resp_artist_resource is None:
        raise ResourceNotFound(f"Artist resource with id of {artist_id} is not found.")
    return resp_artist_resource

def insert_artist_resource(session, data):
    session.add(data)
    session.flush()
    return data

def delete_artist_resource(session, artist_id):
    resp_artist_resource = session.query(Artist).filter_by(artistId=artist_id).first()
    if resp_artist_resource:
        session.delete(resp_artist_resource)
        session.flush()
    else:
        raise ResourceNotFound(f"Artist resource with id of {artist_id} is not found.")
    
def query_playlist_list(session):
    resp_playlist_list = session.query(Playlist).all()
    return resp_playlist_list

def query_playlist_resource(session, playlist_id):
    resp_playlist_resource = session.query(Playlist).filter_by(playlistId=playlist_id).first()
    if resp_playlist_resource is None:
        raise ResourceNotFound(f"playlist resource with id of {playlist_id} is not found.")
    return resp_playlist_resource

def insert_playlist_resource(session, data):
    session.add(data)
    session.flush()
    return data

def delete_playlist_resource(session, playlist_id):
    resp_playlist_resource = session.query(Playlist).filter_by(playlistId=playlist_id).first()
    if resp_playlist_resource:
        session.delete(resp_playlist_resource)
        session.flush()
    else:
        raise ResourceNotFound(f"Playlist resource with id of {playlist_id} is not found.")
    
def insert_song_into_playlist(session, playlist_id, song_id):
    resp_playlist_resource = session.query(Playlist).filter_by(playlistId=playlist_id).first()
    if resp_playlist_resource is None:
        raise ResourceNotFound(f"playlist resource with id of {playlist_id} is not found.")
    
    resp_song_resource = session.query(Song).filter_by(songId=song_id).first()
    if resp_song_resource is None:
        raise ResourceNotFound(f"Song resource with id of {song_id} is not found.")
    
    playlist_song_association = PlaylistSongAssociation(playlist_id, song_id)
    session.add(playlist_song_association)
    session.flush()

    return playlist_song_association

def get_song_association_list_from_playlist(session, playlist_id):
    #resp_playlist_song_association_list = session.query(PlaylistSongAssociation).filter_by(playlistId=playlist_id).all()
    playlist = session.query(Playlist).options(joinedload(Playlist.song_associations).joinedload(PlaylistSongAssociation.song)).filter(Playlist.playlistId == playlist_id).first()
    if playlist:
        return playlist.song_associations
    else:
        raise ResourceNotFound(f"Playlist resource with id of {playlist_id} is not found.")
    
def insert_song_association_resource_into_playlist(session, data):
    session.add(data)
    session.flush()
    return data
    
def remove_song_from_playlist(session, playlist_id, song_id):
    resp_playlist_song_association_resource = session.query(PlaylistSongAssociation).filter_by(playlistId=playlist_id, song_id=song_id).first()
    if resp_playlist_song_association_resource:
        session.remove(resp_playlist_song_association_resource)
        session.flush()
    else:
        raise ResourceNotFound(f"Song resource with id of {song_id} is not in Playlist resource with id of {playlist_id}.")

def insert_user_resource(session, data):
    #TODO: Work on this
    session.add(data)
    session.flush()
    return data

def query_user_by_username(session, username):
    resp_user_resource = session.query(User).filter(User.username == username).first()
    if resp_user_resource:
        return resp_user_resource
    else:
        raise ResourceNotFound(f"User resource with id of {username} does not exist.")