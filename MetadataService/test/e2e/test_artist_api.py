import pytest, json

def generate_song_dict():
    return {
        "title": "Season of the Witch"
    }

def generate_artist_dict():
    return {
        "name": "Donovan"
    }



@pytest.mark.usefixtures('populate_artist_data')
def test_get_artist_list(client):
    resp = client.get(f"/artists/")
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'success'
    assert error == None

    assert any("artistId" in item.keys() for item in value)
    assert all("artistId" in item.keys() for item in value)
    assert all("name" in item.keys() for item in value)

@pytest.mark.usefixtures('populate_artist_data')
def test_get_artist_resource(client):
    resp = client.get(f"/artists/1")
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'success'
    assert error == None

    assert "artistId" in value.keys() 
    assert "name" in value.keys()

@pytest.mark.usefixtures('populate_artist_data')
def test_create_artist_resource(client):
    test_artist_dict = generate_artist_dict()
    resp = client.post(f"/artists/", data=json.dumps(test_artist_dict), content_type='application/json')

   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 201
    assert message == 'success'
    assert error == None

    assert "artistId" in value.keys() 
    assert "name" in value.keys()
