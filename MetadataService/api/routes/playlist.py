import traceback
from flask import Blueprint, request, g
from marshmallow import ValidationError

from adapters import db_ops
from domain.schema import PlaylistSchema, PlaylistSongAssociationSchema, SongAssociationRequestSchema
from api.responses import (
    response_with,
    SUCCESS_200,
    SUCCESS_201
)

playlist_bp = Blueprint('playlists', __name__)

@playlist_bp.route('/', methods=["GET"])
def get_playlist_list():
    session = g.db_session
    schema = PlaylistSchema(many=True)

    obj_playlist_list = db_ops.query_playlist_list(session)
    dict_playlist_list = schema.dump(obj_playlist_list)

    return response_with(SUCCESS_200, dict_playlist_list)

@playlist_bp.route('/<playlist_id>', methods=["GET"])
def get_playlist_resource(playlist_id):
    session = g.db_session
    schema = PlaylistSchema()

    obj_playlist_resource = db_ops.query_playlist_resource(session, playlist_id)
    dict_playlist_resource = schema.dump(obj_playlist_resource)

    return response_with(SUCCESS_200, dict_playlist_resource)

@playlist_bp.route('/', methods=["POST"])
def create_playlist_resource():
    session = g.db_session
    schema = PlaylistSchema()
    try:
        data = request.json
        obj_playlist_resource = schema.load(data)
        obj_playlist_resource_persisted = db_ops.insert_playlist_resource(session, obj_playlist_resource)
        dict_playlist_resource_persisted = schema.dump(obj_playlist_resource_persisted)

        return response_with(SUCCESS_201, dict_playlist_resource_persisted)
    except Exception as e:
        print(e.msg)


@playlist_bp.route('/<playlist_id>/songs', methods=['GET'])
def get_songs_association_list_from_playlist(playlist_id):
    session = g.db_session
    schema = PlaylistSongAssociationSchema(many=True)

    obj_song_association_list = db_ops.get_song_association_list_from_playlist(session, int(playlist_id))
    dict_song_association_list = schema.dump(obj_song_association_list)

    return response_with(SUCCESS_200, dict_song_association_list)

@playlist_bp.route('/<playlist_id>/songs', methods=['POST'])
def create_song_association_in_playlist(playlist_id):
    session = g.db_session
    req_schema = SongAssociationRequestSchema()
    schema = PlaylistSongAssociationSchema()
    try:
        data = req_schema.load(request.json)
        data.update({"playlistId": int(playlist_id)})
        obj_song_association_resource = schema.load(data)
        obj_song_association_resource_persisted = db_ops.insert_song_association_resource_into_playlist(session, obj_song_association_resource)
        _ = obj_song_association_resource_persisted.song
        dict_song_association_resource_persisted = schema.dump(obj_song_association_resource_persisted)
    except ValidationError as e:
        #traceback.print_exc()
        print(e.messages)
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass

    return response_with(SUCCESS_201, dict_song_association_resource_persisted)


