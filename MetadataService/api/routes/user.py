import traceback
from flask import Blueprint, request, g
from werkzeug.security import generate_password_hash, check_password_hash
from adapters import db_ops
from domain.schema import UserSchema, UserRequestSchema
from utils.auth import encode_auth_token
from api.middleware.auth import require_role
from api.responses import (
    SUCCESS_200,
    response_with,
    SUCCESS_201,
    ERROR_500
)

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    session = g.db_session
    req_schema = UserRequestSchema()
    schema = UserSchema()

    try:
        data = req_schema.dump(request.json)
        hashed_password = generate_password_hash(data['password'])
        data.update({
            'password': hashed_password
        })
        obj_user_resource = schema.load(data)
        obj_user_resource_persisted = db_ops.insert_user_resource(session, obj_user_resource)
        dict_user_resource = schema.dump(obj_user_resource_persisted)
        session.commit()
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass

    # Validate input using Marshmallow Schema
    # Check if user is in database
    # Generate hash using password user has created
    # Create user in database
    # Log user in
    return response_with(SUCCESS_201, dict_user_resource)

@user_bp.route('/login', methods=['POST'])
def login():
    # Find user by either email or username
    # Verify hash of password that was sent in
    # Return an access token back to the user 
    session = g.db_session

    data = request.json
    username = data.get('username', None)
    password = data.get('password', None)
    if not username or not password:
        print('Invalid Credentials!')
    try:
        obj_user_resource = db_ops.query_user_by_username(session, username)
        if not check_password_hash(obj_user_resource.password, password):
            raise Exception("password wrong!")
        access_token = encode_auth_token(obj_user_resource.userId)
        return response_with(SUCCESS_200, access_token)
    except Exception as e:
        traceback.print_exc()
        print("Exception!")


@user_bp.route('/protected', methods=['GET'])
@require_role('user')
def protected_route():
    user_info = {
        'user_id': g.user_id,
        'roles': g.roles
    }

    return response_with(SUCCESS_200, user_info)
