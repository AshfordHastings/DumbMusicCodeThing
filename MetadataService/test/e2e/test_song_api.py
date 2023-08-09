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


@pytest.mark.usefixtures('populate_artist_data', 'populate_song_data')
def test_get_song_list(client, test_user_jwt):
    headers = get_auth_header(test_user_jwt)
    resp = client.get(f"/songs/", headers=headers)
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'success'
    assert error == None

    assert any("songId" in item.keys() for item in value)
    assert all("songId" in item.keys() for item in value)
    assert all("artistId" in item.keys() for item in value)

@pytest.mark.usefixtures('populate_artist_data', "populate_song_data")
def test_get_song_resource(client, test_user_jwt):
    headers = get_auth_header(test_user_jwt)
    resp = client.get(f"/songs/1", headers=headers)
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'success'
    assert error == None

    assert "songId" in value.keys() 
    assert "artistId" in value.keys()
    assert "title" in value.keys()

# #@pytest.mark.usefixtures('populate_artist_data', 'populate_song_data')
# def test_create_song_resource(client):
#     test_song_dict = generate_song_dict()

#     resp = client.post(f"/songs/", data=json.dumps(test_song_dict), content_type='application/json')

   
#     message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

#     assert resp.status_code == 201
#     assert message == 'success'
#     assert error == None

#     assert "songId" in value.keys() 
#     assert "title" in value.keys()

def test_create_song_with_artist_resource(client, test_admin_jwt):
    headers = get_auth_header(test_admin_jwt)
    test_artist_dict = generate_artist_dict()
    test_song_dict = generate_song_dict()

    resp = client.post(f"/artists/", data=json.dumps(test_artist_dict), content_type='application/json', headers=headers)
    value = resp.json.get('value', None)
    assert not None

    test_song_dict.update({'artistId': value['artistId']})
    resp = client.post(f"/songs/", data=json.dumps(test_song_dict), content_type='application/json', headers=headers)

    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 201
    assert message == 'success'
    assert error == None

    assert "songId" in value.keys() 
    assert "artistId" in value.keys()
    assert "title" in value.keys()