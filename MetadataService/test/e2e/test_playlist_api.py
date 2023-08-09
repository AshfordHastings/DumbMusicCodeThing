import pytest, json
from test.util.auth import get_auth_header

def generate_artist_dict():
    return {
        "name": "Donovan"
    }

def generate_song_dict():
    return {
        "title": "Season of the Witch"
    }

def generate_playlist_dict():
    return {
        "name": "Test Playlist"
    }

def test_create_playlist(client, test_user_with_permissions_jwt):
    # Create a new playlist
    headers = get_auth_header(test_user_with_permissions_jwt)
    test_playlist_dict = generate_playlist_dict()
    resp = client.post(f"/playlists/", data=json.dumps(test_playlist_dict), content_type='application/json', headers=headers)
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 201
    assert message == 'success'
    assert error == None

    assert "playlistId" in value.keys() 
    assert "name" in value.keys()

@pytest.mark.usefixtures('populate_artist_data', 'populate_song_data')
def test_add_song_to_playlist(client, test_user_with_permissions_jwt):
    headers = get_auth_header(test_user_with_permissions_jwt)
    test_playlist_dict = generate_playlist_dict()

    # Create Playlist
    resp = client.post(f"/playlists/", data=json.dumps(test_playlist_dict), content_type='application/json', headers=headers)
    playlist_id = resp.json['value']['playlistId']


    resp = client.post(f"/playlists/{playlist_id}/songs", data=json.dumps({"songId": 1}), content_type='application/json', headers=headers)
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 201
    assert message == 'success'
    assert error == None

    assert "date_added" in value.keys() 
    assert "songId" in value.keys()
    assert "playlistId" in value.keys()
    assert "song" in value.keys()

@pytest.mark.usefixtures('populate_playlist_data')
def test_get_songs_in_playlist(client, test_user_with_permissions_jwt):
    headers = get_auth_header(test_user_with_permissions_jwt)
    resp = client.get(f"/playlists/1/songs", headers=headers)
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'success'
    assert error == None

    assert all("songId" in item.keys() for item in value)
    assert all("playlistId" in item.keys() for item in value)
    assert all("date_added" in item.keys() for item in value)
    assert True
    # # Attempt to add a non-existing song to the playlist
    # response_non_existing_song = add_song_to_playlist("Playlist for Song", "Non-Existing Song")
    # assert response_non_existing_song.status_code == 404
    # assert "Song not found" in response_non_existing_song.json["message"]

    # # Attempt to add a song to a non-existing playlist
    # response_non_existing_playlist = add_song_to_playlist("Non-Existing Playlist", "Song for Playlist")
    # assert response_non_existing_playlist.status_code == 404
    # assert "Playlist not found" in response_non_existing_playlist.json["message"]



