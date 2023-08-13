from flask import Blueprint, g, request

from adapters import db_ops
from domain.schema import SongSchema
from api.middleware.auth import require_role
from util.responses import (
    response_with,
    SUCCESS_200,
    SUCCESS_201,
    SUCCESS_204
)

song_bp = Blueprint('songs', __name__)

@song_bp.route('/', methods=['GET'])
@require_role('user')
def get_song_list():
    session = g.db_session
    schema = SongSchema(many=True)

    obj_song_list = db_ops.query_song_list(session)
    dict_song_list = schema.dump(obj_song_list)

    return response_with(SUCCESS_200, dict_song_list)

@song_bp.route('/<song_id>', methods=["GET"])
@require_role('user')
def get_song_resource(song_id):
    session = g.db_session
    schema = SongSchema()

    obj_song_resource = db_ops.query_song_resource(session, song_id)
    dict_song_resource = schema.dump(obj_song_resource)

    return response_with(SUCCESS_200, dict_song_resource)

@song_bp.route('/', methods=["POST"])
@require_role('admin')
def create_song_resource():
    session = g.db_session
    schema = SongSchema()
    try:
        data = request.json
        obj_song_resource = schema.load(data)
        obj_song_resource_persisted = db_ops.insert_song_resource(session, obj_song_resource)
        dict_song_resource_persisted = schema.dump(obj_song_resource_persisted)
    except Exception as e:
        print(e)
        pass

    return response_with(SUCCESS_201, dict_song_resource_persisted)


@song_bp.route('/<song_id>', methods=["DELETE"])
@require_role('admin')
def remove_song_resource(song_id):
    session = g.db_session

    try:
        db_ops.delete_song_resource(session, song_id)
    except Exception as e:
        print(e)
        pass

    return response_with(SUCCESS_204)

