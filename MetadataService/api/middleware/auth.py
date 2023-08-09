from flask import request, g
from functools import wraps

from utils.auth import decode_auth_token
from api.responses import (
    response_with,
    ERROR_401
)

def load_jwt_claims():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace('Bearer ', '')
    
    if not token:
        return response_with(ERROR_401, errors='Token is missing!')

    jwt_claims = decode_auth_token(token)
    g.user_id = jwt_claims.get('sub')
    g.roles = jwt_claims.get('roles', [])
    
def require_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if role_name not in g.roles:
                response_with(ERROR_401, errors='Not Authenticated')
            else:
                return f(*args, **kwargs)
        return wrapped
    return decorator


def token_required(f):
    """Decorator to ensure that a resource is accessed with valid token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        
        if not token:
            return response_with(ERROR_401, errors='Token is missing!')

        current_user_id = decode_auth_token(token)
        if isinstance(current_user_id, str):
            # Error occurred in decoding
            return response_with(ERROR_401)
            #return jsonify({'message': current_user_id}), 401

        return f(current_user_id, *args, **kwargs)

    return decorated