from factory_boy.md.md_factories import (
    ArtistFactory,
    SongFactory,
    PlaylistFactory,
    PlaylistSongAssociationFactory
)
from factory_boy.db import Session

def generate_artists_and_songs(session, num_artists=10, num_songs=10):
    artists = [ArtistFactory(_session=session) for _ in range(num_artists)]
    session.bulk_save_objects(artists)

    songs = [SongFactory(_session=session, artist=artist) for artist in artists for _ in range(num_songs)]
    session.bulk_save_objects(songs)
    return artists, songs

def generate_playlists_from_songs(session, songs, num_playlists=5, songs_per_playlist=10):
    playlists = [PlaylistFactory(_session=session) for _ in range(num_playlists)]
    session.bulk_save_objects(playlists)

    song_index = 0
    for playlist in playlists:
        end_index = min(song_index + songs_per_playlist, len(songs))
        playlist_songs = [PlaylistSongAssociationFactory(_session=session, playlist=playlist, song=song) for song in songs[song_index:end_index]]
        session.bulk_save_objects(playlist_songs)
        song_index = end_index % len(songs)

    return playlists

def seed_metadata_db():
    session = Session()
    try:
        artists, songs = generate_artists_and_songs(session, 20, 30)
        session.flush()

        generate_playlists_from_songs(session, songs)
        session.flush()
    except Exception as e:
        print(e)
        session.rollback()
    session.commit()

    


if __name__ == "__main__":
    seed_metadata_db()