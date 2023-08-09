import json

def generate_user_dict():
    return {
        "username": "testuser1",
        "password": "testpass123",
        "email": "testuser@testing.com",
        "displayName": "Test User 1"
    }

def test_create_user(client):
    # Create a new playlist
    test_user_dict = generate_user_dict()
    resp = client.post(f"/users/", data=json.dumps(test_user_dict), content_type='application/json')
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 201
    assert message == 'success'
    assert error == None

    assert "userId" in value.keys() 
    #assert not "password" in value.keys() 
    assert "username" in value.keys()