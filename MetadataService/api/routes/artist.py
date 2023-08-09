from flask import Blueprint, request, g

from adapters import db_ops
from domain.schema import ArtistSchema
from api.middleware.auth import require_role
from api.responses import (
    response_with,
    SUCCESS_200,
    SUCCESS_201,
    SUCCESS_204
)

artist_bp = Blueprint('artists', __name__)

@artist_bp.route('/', methods=["GET"])
@require_role('user')
def get_artist_list():
    session = g.db_session
    schema = ArtistSchema(many=True)

    obj_artist_list = db_ops.query_artist_list(session)
    dict_artist_list = schema.dump(obj_artist_list)

    return response_with(SUCCESS_200, dict_artist_list)

@artist_bp.route('/<artist_id>', methods=["GET"])
@require_role('user')
def get_artist_resource(artist_id):
    session = g.db_session
    schema = ArtistSchema()

    obj_artist_resource = db_ops.query_artist_resource(session, artist_id)
    dict_artist_resource = schema.dump(obj_artist_resource)

    return response_with(SUCCESS_200, dict_artist_resource)

@artist_bp.route('/', methods=["POST"])
@require_role('admin')
def create_artist_resource():
    session = g.db_session
    schema = ArtistSchema()
    try:
        data = request.json
        obj_artist_resource = schema.load(data)
        obj_artist_resource_persisted = db_ops.insert_artist_resource(session, obj_artist_resource)
        dict_artist_resource_persisted = schema.dump(obj_artist_resource_persisted)
    except Exception as e:
        print(e)


    return response_with(SUCCESS_201, dict_artist_resource_persisted)

@artist_bp.route('/<artist_id>', methods=["DELETE"])
@require_role('admin')
def remove_artist_resource(artist_id):
    session = g.db_session

    try:
        db_ops.delete_artist_resource(session, artist_id)
    except Exception as e:
        print(e)
        pass

    return response_with(SUCCESS_204)
