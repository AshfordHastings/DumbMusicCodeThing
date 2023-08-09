import datetime
import jwt

JWT_SECRET = 'testsecret12345'

def encode_auth_token(user_id):
    # Should I use user_id for this?
    try:
        payload = {
            'iss': 'MetadataService',
            'exp': datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return token
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise e
    except jwt.InvalidTokenError as e:
        raise e
    