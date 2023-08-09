import json
import pytest
from utils.auth import decode_auth_token

def generate_user_dict():
    return {
        "username": "testuser1",
        "password": "testpass123",
        "email": "testuser@testing.com",
        "displayName": "Test User 1"
    }

def generate_user_login_dict():
    return {
        "username": "testuser1",
        "password": "testpass123",
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

def test_login_user(client):
    # Create a new playlist
    test_user_dict = generate_user_dict()
    test_user_login_dict = generate_user_login_dict()

    resp_create = client.post(f"/users/", data=json.dumps(test_user_dict), content_type='application/json')
    user_id = resp_create.json['value']['userId']

    assert resp_create.status_code == 201

    resp = client.post(f"/users/login", data=json.dumps(test_user_login_dict), content_type='application/json')

    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'success'
    assert error == None

    decoded_token = decode_auth_token(value)

    assert decoded_token.get('sub') == user_id

def test_protected_user_route(client, test_user, test_user_jwt):
    headers = {
        "Authorization": f"Bearer {test_user_jwt}"
    }
    resp = client.get("/users/protected", headers=headers)

    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert 'user' in value['roles']
    assert test_user['userId'] == value['user_id']



    
