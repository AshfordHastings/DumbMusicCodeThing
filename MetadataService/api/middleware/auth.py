from flask import request, g
from functools import wraps

from utils.auth import decode_auth_token
from api.responses.response_with import (
    response_with,
)
from api.responses.responses import (
    UNAUTHORIZED_401,
)

def init_app(app):
    @app.before_request
    def init_jwt_auth():
        load_jwt_claims()


def has_permission(permission, user_id, **kwargs):
    resource, action, scope = permission.split(':')
    
    # Check sddgeneral permission
    if f"{resource}:{action}:any" in g.permissions:
        return True

    # Check ownership if relevant
    if f"{resource}:{action}:own" in g.permissions:
        # The ownership check will depend on your application's logic
        # For example, check if user_id matches the owner of the resource

        return True

        #TODO: Implement this!
        # resource_id = kwargs.get(f"{resource}_id")
        # if is_owner(user_id, resource, resource_id):  # Implement this function
        #     return True

    # Additional checks, like collaborative permissions, could go here

    return False
    

def load_jwt_claims():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace('Bearer ', '')
    
    if not token:
        return response_with(UNAUTHORIZED_401, errors='Token is missing!')

    jwt_claims = decode_auth_token(token)
    g.user_id = jwt_claims.get('sub')
    g.permissions = jwt_claims.get('permissions', [])
    g.roles = jwt_claims.get('roles', [])
    
def require_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if role_name not in g.roles:
                response_with(UNAUTHORIZED_401, errors='Not Authenticated')
            else:
                return f(*args, **kwargs)
        return wrapped
    return decorator

def require_permissions(*permissions):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                user_id = g.user_id
                for permission in permissions:
                    #if isinstance(permission, constant)
                    # if permission not in g.permissions:
                    #     response_with(ERROR_401, errors='Not Authenticated')
                    if not has_permission(permission, user_id, **kwargs):
                        #Edit Error handling here - throw error instead of returning ? 
                        return response_with(UNAUTHORIZED_401, errors='Not Authenticated')
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
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
            return response_with(UNAUTHORIZED_401, errors='Token is missing!')

        current_user_id = decode_auth_token(token)
        if isinstance(current_user_id, str):
            # Error occurred in decoding
            return response_with(UNAUTHORIZED_401)
            #return jsonify({'message': current_user_id}), 401

        return f(current_user_id, *args, **kwargs)

    return decorated