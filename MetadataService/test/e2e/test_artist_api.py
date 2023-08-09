import pytest, json
from test.util.auth import get_auth_header

def generate_song_dict():
    return {
        "title": "Season of the Witch"
    }

def generate_artist_dict():
    return {
        "name": "Donovan"
    }



@pytest.mark.usefixtures('populate_artist_data')
def test_get_artist_list(client, test_user_jwt):
    headers = get_auth_header(test_user_jwt)
    resp = client.get(f"/artists/", headers=headers)
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'success'
    assert error == None

    assert any("artistId" in item.keys() for item in value)
    assert all("artistId" in item.keys() for item in value)
    assert all("name" in item.keys() for item in value)

@pytest.mark.usefixtures('populate_artist_data')
def test_get_artist_resource(client, test_user_jwt):
    headers = get_auth_header(test_user_jwt)
    resp = client.get(f"/artists/1", headers=headers)
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'success'
    assert error == None

    assert "artistId" in value.keys() 
    assert "name" in value.keys()

@pytest.mark.usefixtures('populate_artist_data')
def test_create_artist_resource(client, test_admin_jwt):
    headers = get_auth_header(test_admin_jwt)
    test_artist_dict = generate_artist_dict()
    resp = client.post(f"/artists/", data=json.dumps(test_artist_dict), content_type='application/json', headers=headers)

   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 201
    assert message == 'success'
    assert error == None

    assert "artistId" in value.keys() 
    assert "name" in value.keys()
